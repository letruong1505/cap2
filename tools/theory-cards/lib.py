# Công cụ dựng lý thuyết dạng thẻ cho Toán 12.
# Mỗi bài khai báo: summary (một dòng "Cần nhớ"), danh sách thẻ, và vị trí chèn hình (figure -> chỉ số thẻ mà hình đứng sau).
# Hình (figure) và phần "cách giải" (method) được lấy từ chính file bài học nên chạy lại không làm mất.
import json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
BASE = os.path.join(ROOT, 'content', 'toan12')


def use(subject):
    """Đổi môn/lớp đang dựng (mặc định toan12), ví dụ use('ly12')."""
    global BASE
    BASE = os.path.join(ROOT, 'content', subject)


def card(title, text=None, formulas=None, points=None, table=None, tip=None, pit=None, try_=None):
    c = {'type': 'card', 'title': title}
    if text: c['text'] = text
    if formulas: c['formulas'] = formulas
    if points: c['points'] = points
    if table: c['table'] = {'head': table[0], 'rows': table[1:]}
    if pit:  # (sai, đúng, giải thích)
        c['wrong'], c['right'] = pit[0], pit[1]
        if len(pit) > 2: c['why'] = pit[2]
    if tip: c['tip'] = tip
    if try_:  # (câu hỏi, [phương án], chỉ số đúng, giải thích)
        c['try'] = {'q': try_[0], 'options': try_[1], 'answer': try_[2], 'explain': try_[3]}
    return c


def build(rel, summary, cards, figs=None, intro=None):
    """rel: đường dẫn bài so với content/toan12 (không có .json)."""
    path = os.path.join(BASE, rel + '.json')
    d = json.load(open(path, encoding='utf8'))
    old = d['theory']
    figures = [b for b in old if b['type'] == 'figure']
    methods = [b for b in old if b['type'] == 'method']
    figs = figs or {}
    for f in figures:
        if f['figure'] not in figs:
            sys.exit('%s: thiếu vị trí hình %s' % (rel, f['figure']))
    for k in figs:
        if not any(f['figure'] == k for f in figures):
            sys.exit('%s: hình %s không có trong bài' % (rel, k))
    out = [{'type': 'summary', 'label': 'Cần nhớ', 'content': summary}]
    if intro: out.append({'type': 'text', 'content': intro})
    for i, c in enumerate(cards, 1):
        c = dict(c); c['n'] = i
        out.append(c)
        for f in figures:
            if figs[f['figure']] == i: out.append(f)
    out.extend(methods)
    d['theory'] = out
    with open(path, 'w', encoding='utf8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
