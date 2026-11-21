#!/usr/bin/env python3
"""Chuyển lý thuyết dạng đoạn văn sang dạng thẻ một cách tự động (tóm tắt + thẻ có tiêu đề + gạch đầu dòng).
Dùng cho các môn chưa viết tay từng thẻ. Bỏ qua bài đã có thẻ (chạy lại không đổi) và bài ôn tập.
Cách dùng: python3 tools/auto-cards.py hoa12 sinh12 ..."""
import json, os, re, sys, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LABEL = re.compile(r'^([^:.;]{3,70}):\s+(\S.*)$', re.S)
SPLIT = re.compile(r'(?<=[.;])\s+(?=[A-ZÀ-ỴĐ(\[\d“"])')
NUM = re.compile(r'\s*\((\d)\)\s+')


def cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:]


def sentences(body):
    body = body.strip()
    if NUM.search(body) and body.count('(1)'):
        head, *parts = re.split(r'\(\d\)\s+', body)
        out = [p.strip().rstrip(';').strip() for p in parts if p.strip()]
        return ([head.strip()] if head.strip() else []) + out
    return [s.strip() for s in SPLIT.split(body) if s.strip()]


def to_card(text, is_first=False):
    m = LABEL.match(text.strip())
    if m and not re.search(r'[→=]', m.group(1)):
        title, body = cap(m.group(1)), m.group(2)
    else:
        ss = SPLIT.split(text.strip())
        first = ss[0].strip().rstrip('.:;')
        if len(first) <= 60 and len(ss) > 1:
            title, body = cap(first), ' '.join(ss[1:])
        else:
            words = first.split()
            title = 'Khái niệm' if is_first else cap(' '.join(words[:7]).rstrip(',;: ')) + ('…' if len(words) > 7 else '')
            body = text
    pts = [cap(x) for x in sentences(body)]
    c = {'type': 'card', 'title': title}
    if len(pts) == 1 and len(pts[0]) <= 320:
        c['text'] = pts[0]
    else:
        c['points'] = pts
    return c


def summary_of(first_text):
    ss = SPLIT.split(first_text.strip())
    out = ss[0]
    if len(ss) > 1 and len(out) < 90:
        out += ' ' + ss[1]
    return out if len(out) <= 260 else out[:257].rsplit(' ', 1)[0] + '…'


def convert(path):
    d = json.load(open(path, encoding='utf8'))
    th = d.get('theory') or []
    if not th or th[0].get('type') in ('summary',) or any(b['type'] == 'card' for b in th):
        return False
    texts = [b for b in th if b['type'] == 'text']
    if not texts:
        return False
    out = [{'type': 'summary', 'label': 'Cần nhớ', 'content': summary_of(texts[0]['content'])}]
    n = 0
    last = None
    for b in th:
        t = b['type']
        if t == 'text':
            c = to_card(b['content'], is_first=(n == 0)); n += 1; c['n'] = n; out.append(c); last = c
        elif t == 'formula':
            if last is not None:
                last.setdefault('formulas', []).append(b['content'])
            else:
                n += 1; last = {'type': 'card', 'n': n, 'title': 'Công thức', 'formulas': [b['content']]}; out.append(last)
        else:
            out.append(b)
    d['theory'] = out
    with open(path, 'w', encoding='utf8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2); fh.write('\n')
    return True


def main(subjects):
    total = 0
    for s in subjects:
        k = 0
        for p in sorted(glob.glob(os.path.join(ROOT, 'content', s, '**', '*.json'), recursive=True)):
            if p.endswith('manifest.json') or 'on-tap' in p:
                continue
            if convert(p): k += 1
        print(s, k); total += k
    print('Đã chuyển', total, 'bài.')


if __name__ == '__main__':
    main(sys.argv[1:])
