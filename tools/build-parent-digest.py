#!/usr/bin/env python3
"""Tạo bản tóm tắt nội dung Giáo trình văn hóa cho app Phụ huynh: parent/digest/van-hoa-<lớp>.js.
Mỗi bài: yêu cầu cần đạt, kiến thức cần nhớ, dạng bài, các bước giải, lỗi dễ mắc, số câu theo mức.
Không chứa câu hỏi hay đáp án; app Phụ huynh chỉ đọc tóm tắt (tải theo lớp, khi phụ huynh mở)."""
import json, os, re, sys, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'parent', 'digest')
SUBJECTS = [('toan', 'Toán'), ('ly', 'Vật lí'), ('hoa', 'Hoá học'), ('sinh', 'Sinh học'), ('anh', 'Tiếng Anh'),
            ('lichsu', 'Lịch sử'), ('diali', 'Địa lí'), ('gdktpl', 'Giáo dục kinh tế và pháp luật')]
MARK = re.compile(r'\{[svck] ([^{}]*)\}')

def clean(s, n=200):
    s = str(s or '')
    while MARK.search(s): s = MARK.sub(r'\1', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'

def lesson_digest(d, title):
    out = {'t': clean(title, 120)}
    req = [clean(x, 220) for x in (d.get('requirements') or []) if clean(x)][:3]
    if req: out['req'] = req
    sums, methods, errs = [], [], []
    for t in d.get('theory') or []:
        ty = t.get('type')
        if ty == 'summary' and t.get('content'): sums.append(clean(t['content'], 200))
        elif ty == 'card':
            head = clean(t.get('title'), 90)
            body = ''
            if t.get('points'): body = clean(t['points'][0], 150)
            elif t.get('text'): body = clean(t['text'], 150)
            if head and body and len(sums) < 8: sums.append(head + ': ' + body)
            elif head and len(sums) < 8: sums.append(head)
            if t.get('wrong') and t.get('right'):
                e = 'Sai: ' + clean(t['wrong'], 110) + ' → Đúng: ' + clean(t['right'], 110)
                if t.get('why'): e += ' (' + clean(t['why'], 110) + ')'
                errs.append(e)
        elif ty == 'method':
            m = {'t': clean(t.get('title'), 100)}
            if t.get('when'): m['w'] = clean(t['when'], 200)
            if t.get('steps'): m['s'] = [clean(x, 170) for x in t['steps']][:7]
            if t.get('notes'): m['n'] = [clean(x, 170) for x in (t['notes'] if isinstance(t['notes'], list) else [t['notes']])][:3]
            methods.append(m)
    items = d.get('items') or []
    for it in items:
        for k, v in (it.get('wrong_explain') or {}).items():
            c = clean(v, 170)
            if len(c) >= 25 and len(errs) < 6 and c not in errs: errs.append('Hay nhầm: ' + c)
    for m in methods:
        for n in m.get('n', []):
            if len(errs) < 8 and n not in errs: errs.append('Lưu ý: ' + n)
    dang = []
    for it in items:
        x = clean(it.get('dang'), 90)
        if x and x not in dang: dang.append(x)
    if methods: out['m'] = methods[:2]
    if sums: out['sum'] = sums[:6]
    if dang: out['d'] = dang[:6]
    if errs: out['e'] = errs[:6]
    lv = {}
    for it in items:
        if it.get('level'): lv[it['level']] = lv.get(it['level'], 0) + 1
    if items: out['q'] = {'n': len(items), 'lv': lv}
    return out

def build_grade(g):
    subs = []
    for sid, name in SUBJECTS:
        base = os.path.join(ROOT, 'content', sid + str(g))
        mf = os.path.join(base, 'manifest.json')
        if not os.path.exists(mf): continue
        man = json.load(open(mf, encoding='utf8'))
        books = []
        for b in man['books']:
            chs = []
            for c in b['chapters']:
                ls = []
                for l in c['lessons']:
                    if not l.get('file'): continue
                    p = os.path.join(base, l['file'])
                    if not os.path.exists(p): continue
                    ls.append(lesson_digest(json.load(open(p, encoding='utf8')), l['title']))
                if ls: chs.append({'t': clean(c['title'], 140), 'l': ls})
            if chs: books.append({'t': clean(b['title'], 90), 'c': chs})
        if books: subs.append({'id': sid, 'name': name, 'b': books})
    return {'grade': g, 'subjects': subs}

def main():
    os.makedirs(OUT, exist_ok=True)
    for g in range(6, 13):
        data = build_grade(g)
        js = '// Tạo bởi tools/build-parent-digest.py, không sửa tay.\n(window.PARENT_DIGEST = window.PARENT_DIGEST || {})[%d] = %s;\n' % (g, json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        open(os.path.join(OUT, 'van-hoa-%d.js' % g), 'w', encoding='utf8').write(js)
        print('lớp', g, round(len(js.encode()) / 1024), 'KB', sum(len(l) for s in data['subjects'] for b in s['b'] for c in b['c'] for l in [c['l']]), 'bài')
main()
