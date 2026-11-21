#!/usr/bin/env python3
"""Chuyển các bài ChatGPT (AI cho người đi làm) sang cấu trúc thẻ: tóm tắt đầu bài, mỗi ý nhỏ (h4) một thẻ đánh số,
đoạn dài tách thành gạch đầu dòng, BÀI TẬP thành khung "Thử ngay". Chạy lặp lại an toàn (bỏ qua bài đã chuyển).
Chạy: node tools/dump... không cần; python3 tools/cardify-chatgpt.py"""
import re, json, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
import sys
TARGETS = {'chatgpt': ('renderer/ai-work-chatgpt.js', 'AI_WORK_CHATGPT'), 'chung': ('renderer/ai-work-content.js', 'AI_WORK_LESSONS'), 'giasu': ('renderer/gia-su-ai-content.js', 'GIA_SU_AI'), 'claude': ('renderer/ai-work-claude.js', 'AI_WORK_CLAUDE')}
WHICH = sys.argv[1] if len(sys.argv) > 1 else 'chatgpt'
F = ROOT / TARGETS[WHICH][0]
VAR = TARGETS[WHICH][1]
raw = subprocess.check_output(['node', '-e', "global.window={};require('%s');console.log(JSON.stringify(window.%s))" % (F, VAR)])
data = json.loads(raw)
head = '\n'.join(F.read_text(encoding='utf8').split('\n', 2)[:2]) if WHICH == 'giasu' else F.read_text(encoding='utf8').split('\n', 1)[0]

SENT = re.compile(r'(?<=[.!?”])\s+(?=[A-ZÀ-Ỹ“(\[])')
def bullets(p):
    inner = p
    # nhiều mục đậm liên tiếp: "<b>A: </b>... <b>B: </b>..." -> mỗi mục một dòng
    parts = re.split(r'(?=<b>[^<]{2,40}: ?</b>)', inner)
    parts = [x.strip() for x in parts if x.strip()]
    if len(parts) >= 3 or (len(parts) == 2 and all(x.startswith('<b>') for x in parts)):
        return '<ul class="tl">' + ''.join('<li>%s</li>' % x for x in parts) + '</ul>'
    ss = []
    for x in (y.strip() for y in SENT.split(inner) if y.strip()):
        if ss and ss[-1].count('“') > ss[-1].count('”'): ss[-1] += ' ' + x   # giữ nguyên câu trích dẫn
        else: ss.append(x)
    if len(ss) >= 3:
        return '<ul class="tl">' + ''.join('<li>%s</li>' % x for x in ss) + '</ul>'
    return '<p>%s</p>' % inner

def fix_paras(html):
    def one(m):
        t = m.group(1)
        if re.match(r'<b>BÀI TẬP', t):
            t = re.sub(r'^<b>BÀI TẬP[^<]*</b>\s*', '', t)
            return '<div class="ttry"><span class="ttry-l">Thử ngay</span><p>%s</p></div>' % t
        if len(re.sub(r'<[^>]+>', '', t)) > 200: return bullets(t)
        return m.group(0)
    return re.sub(r'<p>(.*?)</p>', one, html, flags=re.S)

def cardify(d):
    h = d['html']
    if 'class="tsum"' in h: return d
    first = re.search(r'<h[34]>', h)
    pre, rest = (h[:first.start()], h[first.start():]) if first else (h, '')
    meta = re.search(r'<div class="meta">(.*?)</div>\s*</div>', pre, flags=re.S)
    items = []
    if meta:
        for lab, val in re.findall(r'<div><b>(.*?)</b>(.*?)(?=</div>|$)', meta.group(1) + '</div>', flags=re.S):
            items.append('<li><b>%s:</b> %s</li>' % (lab, val))
        pre = pre.replace(meta.group(0), '')
    tsum = '<div class="tsum"><div class="tsum-l">Tóm tắt bài</div>%s</div>' % (('<ul>%s</ul>' % ''.join(items)) if items else '<p>%s</p>' % d['sub'])
    h3cards = '<h4>' not in rest   # bài chỉ có h3: mỗi h3 là một thẻ
    if h3cards: rest = rest.replace('<h3>', '<h4>').replace('</h3>', '</h4>')
    parts = re.split(r'(?=<h[34]>)', rest)
    out, n = [], 0
    for seg in parts:
        if not seg: continue
        if seg.startswith('<h3>'):
            m = re.match(r'<h3>(.*?)</h3>(.*)', seg, flags=re.S)
            out.append('<h3 class="tchap">%s</h3>%s' % (m.group(1), fix_paras(m.group(2))))
        else:
            n += 1
            m = re.match(r'<h4>(.*?)</h4>(.*)', seg, flags=re.S)
            title = re.sub(r'^\d+(\.\d+)?\.?\s*', '', m.group(1))
            out.append('<section class="tcard"><h4><span class="tn">%d</span>%s</h4>%s</section>' % (n, title, fix_paras(m.group(2))))
    d['html'] = tsum + fix_paras(pre) + ''.join(out)
    return d

for k in data: data[k] = cardify(data[k])
F.write_text(head + '\nwindow.%s = ' % VAR + json.dumps(data, ensure_ascii=False, indent=1) + ';\n', encoding='utf8')
print({k: (v['html'].count('class="tcard"'), len(v['html'])) for k, v in data.items()})
