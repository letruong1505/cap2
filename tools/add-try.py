#!/usr/bin/env python3
"""Thêm câu "Thử ngay" cho các bài đã có thẻ nhưng chưa có câu thử.
Lấy từ chính các câu trắc nghiệm khái niệm (concept, hoặc mức "Biết" nếu bài không có) của bài, có đáp án và giải thích sẵn, nên không tự bịa nội dung.
Bài đã có câu "Thử ngay" (viết tay) được giữ nguyên; chạy lại không đổi.
Cách dùng: python3 tools/add-try.py [môn ...]  (không ghi môn thì làm tất cả)"""
import json, os, sys, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BAD = ('hình', 'bảng', 'đồ thị', 'sơ đồ', 'biểu đồ', 'đoạn', 'bản đồ', 'ảnh', 'lược đồ')


def pick(items, strict=True):
    out = []
    for i in items:
        if i.get('type') != 'mcq' or (strict and not i.get('concept')) or (not strict and i.get('level') != 'Biết'):
            continue
        if any(k in i for k in ('figure', 'expr', 'reading')):
            continue
        ch = i.get('choices') or []
        if not (2 <= len(ch) <= 4) or len(set(ch)) != len(ch):
            continue
        a = i.get('answer')
        if not isinstance(a, int) or not (0 <= a < len(ch)) or not i.get('explain') or not i.get('stem'):
            continue
        low = i['stem'].lower()
        if len(i['stem']) > 240 or any(w in low for w in BAD):
            continue
        out.append({'q': i['stem'], 'options': ch, 'answer': a, 'explain': i['explain']})
    return out


def convert(path):
    d = json.load(open(path, encoding='utf8'))
    th = d.get('theory') or []
    cards = [b for b in th if b['type'] == 'card']
    if not cards or any(c.get('try') for c in cards):
        return 0
    qs = pick(d.get('items') or []) or pick(d.get('items') or [], False)
    if not qs:
        return 0
    spots = [cards[min(len(cards) - 1, max(0, len(cards) // 3))]]
    if len(cards) >= 4 and len(qs) >= 2 and cards[-1] is not spots[0]:
        spots.append(cards[-1])
    n = 0
    for c, q in zip(spots, qs):
        c['try'] = q; n += 1
    with open(path, 'w', encoding='utf8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2); fh.write('\n')
    return n


def main(subjects):
    subjects = subjects or sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'content', '*')))
    lessons = tries = 0
    for s in subjects:
        for p in sorted(glob.glob(os.path.join(ROOT, 'content', s, '**', '*.json'), recursive=True)):
            if p.endswith('manifest.json') or 'on-tap' in p or 'nang-cao' in p or 'de-thi' in p:
                continue
            n = convert(p)
            if n: lessons += 1; tries += n
    print('Đã thêm', tries, 'câu "Thử ngay" cho', lessons, 'bài.')


if __name__ == '__main__':
    main(sys.argv[1:])
