// Mục "Định hướng công nghệ quốc gia": chiến lược quốc gia, danh mục công nghệ, chọn hướng và kế hoạch học tập.
// Chạy hoàn toàn offline. Mọi chữ được gán bằng textContent (hàm h) nên không chèn mã HTML.

(function () {
  const D = window.NATIONAL_DATA;
  const KEY = 'nl-dhcnqg';

  const h = (tag, attrs, ...children) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === undefined || v === null || v === false) continue;
      if (k === 'class') n.className = v;
      else if (k.startsWith('on') && typeof v === 'function') n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v === true ? '' : v);
    }
    for (const c of children.flat()) {
      if (c === undefined || c === null || c === false) continue;
      n.append(c instanceof Node ? c : String(c));
    }
    return n;
  };
  const chips = (arr) => h('div', { class: 'nat-chips' }, arr.map((x) => h('span', {}, x)));
  const ul = (arr) => h('ul', { class: 'nat-list' }, arr.map((x) => h('li', {}, x)));

  const TABS = [
    ['tong-quan', 'Tổng quan chiến lược'],
    ['van-ban', 'Văn bản và hiệu lực'],
    ['nhom', '10 nhóm công nghệ'],
    ['ke-hoach', 'Kế hoạch của em'],
    ['nguon', 'Nguồn tham khảo'],
  ];

  const SOURCES = [
    ['1', 'Nghị quyết 57-NQ/TW', 'Văn bản gốc', '22/12/2024', 'Bộ Chính trị: đột phá phát triển khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số quốc gia. Toàn văn đăng trên Cổng thông tin điện tử tỉnh Hà Tĩnh (hatinh.gov.vn).'],
    ['2', 'Nghị quyết 03/NQ-CP', 'Văn bản gốc', '09/01/2025', 'Chính phủ: Chương trình hành động thực hiện Nghị quyết 57. Theo Mekong ASEAN, VGP.'],
    ['3', 'Quyết định 21/2026/QĐ-TTg', 'Văn bản gốc (hiện hành)', '30/04/2026', 'Danh mục công nghệ chiến lược và sản phẩm công nghệ chiến lược, hiệu lực từ 01/07/2026. Theo Tạp chí Công Thương, Thị trường Tài chính Tiền tệ, Báo Đấu thầu, Mekong ASEAN.'],
    ['4', 'Nghị quyết 71-NQ/TW', 'Văn bản gốc', '22/08/2025', 'Bộ Chính trị: đột phá phát triển giáo dục và đào tạo.'],
    ['5', 'Số liệu kinh tế số 2025 (khoảng 14,02% GDP)', 'Số liệu thống kê', '2025', 'Cục Thống kê, Bộ Tài chính, theo báo Đại biểu Nhân dân. Chỉ có một nguồn báo.'],
    ['6', 'Bài “Đường đua kỷ nguyên số”', 'Báo chính thống', '2025', 'VnExpress: mục tiêu xếp hạng và kinh tế số đến năm 2030.'],
    ['7', 'SIFT: bốn bước kiểm chứng thông tin', 'Phương pháp', 'CC BY 4.0', 'Mike Caulfield. Em dùng để tự kiểm tra thông tin trên mạng.'],
  ];

  const DOCS = [
    ['22/12/2024', 'Nghị quyết 57-NQ/TW', 'Bộ Chính trị: đột phá khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số quốc gia.', 'Đang thực hiện', 'ok'],
    ['09/01/2025', 'Nghị quyết 03/NQ-CP', 'Chương trình hành động của Chính phủ thực hiện Nghị quyết 57.', 'Đang thực hiện', 'ok'],
    ['22/08/2025', 'Nghị quyết 71-NQ/TW', 'Đột phá phát triển giáo dục và đào tạo, ứng dụng AI trong giáo dục.', 'Đang thực hiện', 'ok'],
    ['30/04/2026', 'Quyết định 21/2026/QĐ-TTg', 'Danh mục hiện hành: 10 nhóm công nghệ, 30 sản phẩm. Hiệu lực từ 01/07/2026.', 'Có hiệu lực', 'now'],
  ];

  const GOALS = [
    ['Kinh tế', 'TFP đóng góp trên 55% tăng trưởng; kinh tế số tối thiểu 30% GDP; sản phẩm công nghệ cao tối thiểu 50% giá trị xuất khẩu hàng hóa.'],
    ['Dịch vụ số', 'Dịch vụ công trực tuyến trên 80%; giao dịch không dùng tiền mặt 80%; trên 40% doanh nghiệp có đổi mới sáng tạo.'],
    ['Đầu tư', 'Chi R&D đạt 2% GDP (trên 60% từ xã hội); ít nhất 3% tổng chi ngân sách hằng năm cho khoa học, công nghệ và chuyển đổi số.'],
    ['Nhân lực', '12 nhân lực R&D trên một vạn dân; công bố quốc tế tăng bình quân 10%/năm; sáng chế tăng 16–18%/năm.'],
    ['Hạ tầng', 'Phủ sóng 5G toàn quốc; hoàn thành cơ sở dữ liệu quốc gia, hình thành sàn giao dịch dữ liệu.'],
    ['Xếp hạng', 'Nhóm 3 dẫn đầu Đông Nam Á, nhóm 50 đầu thế giới về năng lực cạnh tranh số và Chính phủ điện tử; ít nhất 5 doanh nghiệp công nghệ số ngang tầm các nước tiên tiến.'],
  ];

  const state = { tab: 'tong-quan', group: null, picks: [] };
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || '[]');
    if (Array.isArray(saved)) state.picks = saved.filter((id) => D.groups.some((g) => g.id === id)).slice(0, 3);
  } catch { /* không lưu được thì bỏ qua */ }
  const savePicks = () => { try { localStorage.setItem(KEY, JSON.stringify(state.picks)); } catch { /* bỏ qua */ } };

  let root;
  const goto = (tab, group = null) => { state.tab = tab; state.group = group; render(); root.scrollIntoView({ block: 'start' }); window.scrollTo(0, 0); };

  const head = (title, sub) => h('div', { class: 'nat-head' }, h('h1', {}, title), sub && h('p', { class: 'screen-sub' }, sub));
  const note = (kind, label, text) => h('section', { class: 'nat-card nat-note nat-' + kind }, h('div', { class: 'nat-label' }, label), h('p', {}, text));
  const srcLine = (refs) => h('div', { class: 'nat-source' },
    h('b', {}, 'Nguồn tham khảo'), h('span', {}, refs),
    h('button', { type: 'button', class: 'nat-linkbtn', onclick: () => goto('nguon') }, 'Xem danh sách đầy đủ'));

  // ----- Tổng quan
  function bar(hpx, color, label, value) {
    return h('div', { class: 'nat-bar' }, h('b', {}, value), h('div', { class: 'nat-bar-col', style: `height:${hpx}px;background:${color}` }), h('span', {}, label));
  }
  function stat(n, label, sub, color) {
    return h('div', { class: 'nat-card nat-stat' }, h('div', { class: 'nat-num', style: color ? `color:${color}` : '' }, n), h('div', { class: 'nat-stat-label' }, label), h('div', { class: 'muted' }, sub));
  }
  function viewOverview() {
    return h('div', { class: 'nat-view' },
      head('Chiến lược quốc gia trong một trang', 'Nghị quyết 57-NQ/TW (22/12/2024) đặt khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số làm đột phá hàng đầu, để Việt Nam là nước phát triển, thu nhập cao vào năm 2045.'),
      h('div', { class: 'nat-stats' },
        stat('30%', 'Kinh tế số trong GDP', 'mục tiêu tối thiểu năm 2030', '#2a6db5'),
        stat('50%', 'Kinh tế số trong GDP', 'tầm nhìn tối thiểu năm 2045', '#1f7a4d'),
        stat('10', 'Nhóm công nghệ chiến lược', 'theo Quyết định 21/2026/QĐ-TTg'),
        stat('7', 'Nhóm nhiệm vụ, giải pháp', 'trong Nghị quyết 57')),
      h('div', { class: 'nat-two' },
        h('section', { class: 'nat-card' },
          h('h2', {}, 'Quy mô kinh tế số trong GDP'),
          h('p', { class: 'muted' }, 'Năm 2025 là số ước tính của Cục Thống kê. Hai cột sau là mục tiêu.'),
          h('div', { class: 'nat-bars' },
            bar(70, '#9fb4cc', '2025 (ước tính)', 'khoảng 14%'),
            bar(150, '#2a6db5', 'Mục tiêu 2030', 'tối thiểu 30%'),
            bar(250, '#1f7a4d', 'Tầm nhìn 2045', 'tối thiểu 50%'))),
        h('section', { class: 'nat-card' },
          h('h2', {}, 'Năm quan điểm chỉ đạo'),
          h('ol', { class: 'nat-ol' },
            h('li', {}, 'Đột phá hàng đầu, là động lực chính để không tụt hậu'),
            h('li', {}, 'Cả hệ thống cùng làm; người dân và doanh nghiệp là chủ thể'),
            h('li', {}, 'Thể chế đi trước một bước, cho phép thử nghiệm'),
            h('li', {}, 'Từng bước tự chủ công nghệ, nhất là công nghệ chiến lược'),
            h('li', {}, 'An ninh mạng, an ninh dữ liệu xuyên suốt')),
          h('h2', { class: 'nat-h2gap' }, 'Bảy nhóm giải pháp'),
          chips(['Nhận thức, học tập số', 'Thể chế', 'Hạ tầng và dữ liệu', 'Nhân lực, nhân tài', 'Chuyển đổi số, an ninh mạng', 'Doanh nghiệp', 'Hợp tác quốc tế']))),
      h('section', { class: 'nat-card' },
        h('h2', {}, 'Mục tiêu đến năm 2030'),
        h('table', { class: 'nat-table' }, h('tbody', {}, GOALS.map(([a, b]) => h('tr', {}, h('th', {}, a), h('td', {}, b))))),
        h('p', { class: 'nat-after' }, 'Tầm nhìn 2045: kinh tế số tối thiểu 50% GDP; thuộc nhóm 30 nước dẫn đầu thế giới về đổi mới sáng tạo và chuyển đổi số; ít nhất 10 doanh nghiệp công nghệ số ngang tầm tiên tiến.')),
      h('div', { class: 'nat-actions' }, h('button', { type: 'button', class: 'primary', onclick: () => goto('nhom') }, 'Xem 10 nhóm công nghệ chiến lược →')),
      srcLine('[1] Nghị quyết 57-NQ/TW · [5] Cục Thống kê, Bộ Tài chính · [6] VnExpress'));
  }

  // ----- Văn bản
  function viewDocs() {
    const label = { ok: 'Đang thực hiện', old: 'Đã bị thay thế', now: 'Có hiệu lực' };
    return h('div', { class: 'nat-view' },
      head('Văn bản và hiệu lực', 'Danh mục công nghệ chiến lược đã được thay đổi. Em dùng đúng bản đang có hiệu lực.'),
      h('div', { class: 'nat-docs' }, DOCS.map(([date, name, text, , kind]) =>
        h('div', { class: 'nat-card nat-doc' + (kind === 'old' ? ' nat-dim' : '') },
          h('b', { class: 'nat-date' }, date), h('div', { class: 'nat-docname' }, name), h('p', {}, text),
          h('span', { class: 'nat-badge nat-b-' + kind }, label[kind])))),
      note('plain', 'Dùng văn bản gốc', 'Khi cần trích dẫn chính thức, em dùng văn bản gốc trên Công báo hoặc cổng thông tin của Chính phủ.'),
      srcLine('[1] Nghị quyết 57-NQ/TW · [3] Quyết định 21/2026/QĐ-TTg · [4] Nghị quyết 71-NQ/TW'));
  }

  // ----- 10 nhóm và chi tiết
  const picked = (id) => state.picks.includes(id);
  function togglePick(id) {
    if (picked(id)) state.picks = state.picks.filter((x) => x !== id);
    else if (state.picks.length < 3) state.picks.push(id);
    else { window.alert('Em chọn tối đa 3 hướng. Hãy bỏ bớt một hướng ở mục Kế hoạch của em.'); return false; }
    savePicks();
    return true;
  }

  function viewGroups() {
    const idx = (g) => String(D.groups.indexOf(g) + 1);
    const tiles = D.groups.map((g) => h('button', { type: 'button', class: 'nat-tile' + (picked(g.id) ? ' on' : ''), onclick: () => goto('nhom', g.id), 'aria-label': g.n },
      h('span', { class: 'nat-tilenum' }, idx(g)),
      h('b', {}, g.n), h('span', { class: 'muted' }, g.e),
      chips(g.s)));
    return h('div', { class: 'nat-view' },
      head('10 nhóm công nghệ chiến lược', 'Quyết định 21/2026/QĐ-TTg: 10 nhóm công nghệ và 30 sản phẩm. Chọn một nhóm để xem chi tiết.'),
      h('div', { class: 'nat-tiles' }, tiles),
      h('div', { class: 'nat-three' },
        h('section', { class: 'nat-card nat-slim' }, h('b', {}, '22 sản phẩm nhóm 1'), h('div', { class: 'muted' }, 'Đã có thị trường, tác động lớn và trực tiếp đến phát triển kinh tế.')),
        h('section', { class: 'nat-card nat-slim' }, h('b', {}, '8 sản phẩm nhóm 2'), h('div', { class: 'muted' }, 'Động lực tăng trưởng mới, công nghệ nền tảng tương lai, tự chủ quốc phòng, an ninh.')),
        h('section', { class: 'nat-card nat-slim nat-blue' }, h('b', {}, 'Môn học và ngành gợi ý là của Nam Linh'), h('div', { class: 'muted' }, 'Không phải quy định của văn bản. Em hỏi thầy cô để chọn môn phù hợp.'))),
      srcLine('[3] Quyết định 21/2026/QĐ-TTg'));
  }

  function viewGroup(id) {
    const g = D.groups.find((x) => x.id === id);
    const n = D.groups.indexOf(g) + 1;
    const on = picked(id);
    return h('div', { class: 'nat-view' },
      h('button', { type: 'button', class: 'nat-linkbtn nat-backline', onclick: () => goto('nhom') }, '‹ Quay lại 10 nhóm'),
      h('div', { class: 'nat-grouphead' },
        h('div', {}, h('h1', {}, h('span', { class: 'nat-mark' }, String(n)), ' ' + g.n), h('p', { class: 'screen-sub' }, g.e)),
        h('button', { type: 'button', class: 'primary', onclick: () => { if (togglePick(id)) { if (!on) goto('ke-hoach'); else render(); } } }, on ? 'Bỏ chọn hướng này' : 'Chọn hướng này')),
      h('div', { class: 'nat-three' },
        h('section', { class: 'nat-card' }, h('h2', {}, 'Sản phẩm chiến lược liên quan ', h('span', { class: 'nat-tag' }, 'QĐ 21/2026')), ul(g.p)),
        h('section', { class: 'nat-card' }, h('h2', {}, 'Em cần gì để đi hướng này?'),
          h('div', { class: 'nat-sub' }, 'Môn nền tảng'), chips(g.s),
          h('div', { class: 'nat-sub' }, 'Nhóm ngành đại học gợi ý'), chips(g.m),
          h('div', { class: 'nat-sub' }, 'Kỹ năng cần rèn'), chips(g.k))),
      h('section', { class: 'nat-card nat-blue' }, h('b', {}, 'Gợi ý khởi đầu'),
        h('div', { class: 'nat-two nat-tight' }, h('div', {}, h('b', {}, 'THCS'), ul(g.a)), h('div', {}, h('b', {}, 'THPT'), ul(g.b)))),
      h('p', { class: 'muted' }, 'Môn nền tảng, ngành đại học và việc làm là gợi ý của Nam Linh, không phải quy định của văn bản.'),
      srcLine('[3] Quyết định 21/2026/QĐ-TTg'));
  }

  // ----- Kế hoạch
  function planCard(g) {
    const line = (label, items) => h('tr', {}, h('th', {}, label), h('td', {}, ul(items)), h('td', { class: 'nat-check' }, '☐'));
    return h('section', { class: 'nat-card nat-plan' },
      h('div', { class: 'nat-planhead' }, h('h2', {}, g.n), chips(g.s)),
      h('div', { class: 'nat-sub' }, 'Nhóm ngành gợi ý'), chips(g.m),
      h('div', { class: 'nat-sub' }, 'Kỹ năng cần rèn'), chips(g.k),
      h('table', { class: 'nat-table nat-planbl' },
        h('thead', {}, h('tr', {}, h('th', {}, 'Giai đoạn'), h('th', {}, 'Việc làm cụ thể'), h('th', {}, 'Xong'))),
        h('tbody', {},
          line('THCS (lớp 6–9)', g.a), line('THPT (lớp 10–12)', g.b),
          h('tr', {}, h('th', {}, 'Mục tiêu đo được cho 3 tháng tới'), h('td', {}, 'Em tự viết. Ví dụ: hoàn thành 1 dự án nhỏ, đạt 8 điểm trở lên ở môn nền tảng, đọc 3 nguồn chính thức về nhóm này.'), h('td', { class: 'nat-check' }, '☐')))));
  }
  function viewPlan() {
    const gs = state.picks.map((id) => D.groups.find((g) => g.id === id)).filter(Boolean);
    return h('div', { class: 'nat-view' },
      head('Kế hoạch học tập của em', 'Chọn tối đa 3 hướng ở mục 10 nhóm công nghệ. Kế hoạch tạo theo lựa chọn, em điền mục tiêu của riêng mình.'),
      h('div', { class: 'nat-picks nat-noprint' },
        h('span', { class: 'muted' }, 'Em đã chọn:'),
        gs.map((g) => h('span', { class: 'nat-pick' }, g.n, h('button', { type: 'button', 'aria-label': 'Bỏ ' + g.n, onclick: () => { togglePick(g.id); render(); } }, '×'))),
        gs.length < 3 && h('button', { type: 'button', class: 'nat-add', onclick: () => goto('nhom') }, '+ Thêm một hướng')),
      gs.length ? gs.map(planCard) : h('section', { class: 'nat-card' }, h('p', {}, 'Em chưa chọn hướng nào. Vào mục 10 nhóm công nghệ, mở một nhóm và bấm “Chọn hướng này”.')),
      h('div', { class: 'nat-actions nat-noprint' },
        gs.length > 0 && h('button', { type: 'button', class: 'primary', onclick: () => window.print() }, 'In kế hoạch'),
        gs.length > 0 && h('button', { type: 'button', class: 'nat-secondary', onclick: () => { state.picks = []; savePicks(); render(); } }, 'Chọn lại')),
      h('section', { class: 'nat-card' }, h('h2', {}, 'Khung chung cho mọi hướng'),
        h('table', { class: 'nat-table' }, h('tbody', {},
          h('tr', {}, h('th', {}, 'THCS (lớp 6–9)'), h('td', {}, 'Học chắc Toán, Khoa học tự nhiên, Tin học, Tiếng Anh; khám phá nhiều hướng; học an toàn số và dùng AI đúng cách; làm dự án nhỏ.')),
          h('tr', {}, h('th', {}, 'THPT (lớp 10–12)'), h('td', {}, 'Chọn tổ hợp môn phù hợp hướng đã chọn; luyện thi và dự án thực tế; tìm hiểu ngành đại học, nghề nghiệp; tham gia cuộc thi, câu lạc bộ.')),
          h('tr', {}, h('th', {}, 'Sau THPT'), h('td', {}, 'Chọn ngành, trường; học thêm kỹ năng mềm, ngoại ngữ; thực tập, tham gia nghiên cứu hoặc doanh nghiệp công nghệ.'))))),
      srcLine('[3] Quyết định 21/2026/QĐ-TTg · gợi ý môn học, ngành: Nam Linh'));
  }

  // ----- Nguồn
  function viewSources() {
    return h('div', { class: 'nat-view' },
      head('Nguồn tham khảo', 'Mọi số liệu trong mục này đều có nguồn. Em nên mở văn bản gốc để kiểm tra lại.'),
      h('section', { class: 'nat-card nat-tablecard' },
        h('table', { class: 'nat-table nat-wide' },
          h('thead', {}, h('tr', {}, ['#', 'Nguồn', 'Loại', 'Ngày', 'Ghi chú'].map((t) => h('th', {}, t)))),
          h('tbody', {}, SOURCES.map(([n, t, k, d, nt]) => h('tr', {}, h('td', { class: 'nat-ref' }, `[${n}]`), h('td', {}, h('b', {}, t)), h('td', {}, h('span', { class: 'nat-badge nat-b-' + (k.includes('thay thế') ? 'old' : k.startsWith('Văn bản') ? 'now' : 'plain') }, k)), h('td', {}, d), h('td', {}, nt)))))),
      h('div', { class: 'nat-two' },
        note('plain', 'Ngày tổng hợp', 'Tháng 11/2026. Danh mục có thể còn được điều chỉnh, em kiểm tra văn bản mới nhất.'),
        note('warn', 'Cần xác minh trước khi dùng chính thức', 'Nội dung tổng hợp từ các nguồn trên, chưa đối chiếu toàn văn trên Công báo. Môn nền tảng và ngành học là gợi ý của Nam Linh.')));
  }

  function render() {
    if (!root) return;
    const nav = h('nav', { class: 'nat-nav nat-noprint', 'aria-label': 'Các mục' }, TABS.map(([id, label], i) =>
      h('button', { type: 'button', class: 'nat-navitem' + (state.tab === id ? ' on' : ''), onclick: () => goto(id), 'aria-current': state.tab === id ? 'page' : false },
        h('span', {}, String(i + 1)), label, id === 'ke-hoach' && state.picks.length ? h('em', {}, String(state.picks.length)) : null)));
    let view;
    if (state.tab === 'van-ban') view = viewDocs();
    else if (state.tab === 'nhom') view = state.group ? viewGroup(state.group) : viewGroups();
    else if (state.tab === 'ke-hoach') view = viewPlan();
    else if (state.tab === 'nguon') view = viewSources();
    else view = viewOverview();
    root.replaceChildren(h('div', { class: 'nat-layout' },
      h('aside', { class: 'nat-side nat-noprint' },
        h('span', { class: 'nat-free' }, 'Miễn phí'),
        h('h2', {}, 'Định hướng công nghệ quốc gia'),
        h('p', { class: 'muted' }, 'Nghị quyết 57 và danh mục công nghệ chiến lược, để em chọn hướng đi và lập kế hoạch học tập.'),
        nav,
        h('p', { class: 'muted nat-upd' }, 'Cập nhật 11/2026. Số liệu có nguồn.')),
      view));
  }

  window.National = {
    open() { root = document.getElementById('national-body'); state.tab = 'tong-quan'; state.group = null; render(); },
  };
})();
