#!/usr/bin/env python3
"""Dựng đề thi thử theo cấu trúc thi tốt nghiệp THPT từ ngân hàng câu hỏi có sẵn của môn (hiện: Toán 12).
Cấu trúc (Quyết định 764/QĐ-BGDĐT): 90 phút, 22 câu.
  Phần I : 12 câu trắc nghiệm 4 phương án, 0,25 điểm/câu.
  Phần II: 4 câu đúng–sai, mỗi câu 4 ý; đúng 1/2/3/4 ý được 0,1/0,25/0,5/1 điểm.
  Phần III: 6 câu trả lời ngắn, 0,5 điểm/câu.
Mọi câu lấy nguyên từ các bài học (đáp án, lời giải đã kiểm tra); không chép đề từ nơi khác.
Câu đúng–sai tạo từ câu trắc nghiệm: mỗi phương án là một ý, ý đúng là phương án đáp án, 3 ý còn lại sai.
Đề được tạo cố định theo hạt giống nên chạy lại cho kết quả giống hệt; các đề không dùng chung câu.
Cách dùng: python3 tools/build-exams.py"""
import json, os, random, glob, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CONTENT = os.path.join(ROOT, 'content')
CHAPTER_KEY = {'chuong-1': 'c1', 'chuong-2': 'c2', 'chuong-3': 'c3', 'chuong-4': 'c4', 'chuong-5': 'c5', 'chuong-6': 'c6', 'on-tap-cuoi-nam': 'ct'}

CONFIG = {
    'toan12': {
        'exams': 3,
        # Số câu theo chương (phân bố giống đề thật: giải tích nhiều nhất, rồi hình học tọa độ, xác suất thống kê).
        'p1': {'c1': 3, 'c2': 1, 'c3': 1, 'c4': 3, 'c5': 2, 'c6': 1, 'ct': 1},
        'p2': ['c1', 'c4', 'c5', 'c2'],
        'p3': ['c1', 'c3', 'c4', 'c5', 'c6', 'c2'],
    },
}


def chapter_of(rel):
    for part in rel.split('/'):
        if part in CHAPTER_KEY:
            return CHAPTER_KEY[part]
    return ''


def load_pool(subject):
    mcq, fill = {}, {}
    base = os.path.join(CONTENT, subject)
    for f in sorted(glob.glob(os.path.join(base, '**', '*.json'), recursive=True)):
        rel = os.path.relpath(f, base).replace(os.sep, '/')
        if rel == 'manifest.json' or rel.startswith('de-thi/'):
            continue
        d = json.load(open(f, encoding='utf8'))
        ch = chapter_of(rel)
        for it in d.get('items', []):
            if not it.get('stem'):
                continue
            ref = {'lesson': rel, 'id': it['id']}
            if it['type'] == 'mcq' and len(it['choices']) == 4 and len(set(it['choices'])) == 4 and it.get('explain'):
                mcq.setdefault(ch, []).append((it, ref, d.get('chapter', '')))
            elif it['type'] == 'fill' and it.get('expr') and it.get('explain'):
                fill.setdefault(ch, []).append((it, ref, d.get('chapter', '')))
    return mcq, fill


def take(rng, pool, ch, used, prefer):
    """Lấy một câu chưa dùng trong chương ch, ưu tiên mức độ trong prefer (theo thứ tự)."""
    cand = [x for x in pool.get(ch, []) if (x[1]['lesson'], x[1]['id']) not in used]
    if not cand:
        raise SystemExit(f'Hết câu cho chương {ch}')
    for lv in prefer:
        sub = [x for x in cand if x[0].get('level') == lv]
        if sub:
            x = rng.choice(sub)
            break
    else:
        x = rng.choice(cand)
    used.add((x[1]['lesson'], x[1]['id']))
    return x


def strip_ref(t):
    """Bỏ số bài tập sách giáo khoa ở đầu hoặc cuối đề ("Bài 3.5: ...", "(Bài 1.17)") vì trong đề thi không có."""
    t = re.sub(r'^((Bài|BT|Hình|Ví dụ)\s+)?\d+\.\d+[a-z]?\s*[:.]\s*', '', t)
    t = re.sub(r'^Luyện tập\s*\d+[a-z]?\s*[:.]\s*', '', t)
    t = re.sub(r"\s*\((Bài|Ví dụ|Luyện tập)\s*\d+(\.\d+)?[a-z]?\)\s*$", "", t)
    return t[:1].upper() + t[1:] if t else t


def clean(it, new_id, part, ref, topic):
    keep = ('level', 'type', 'stem', 'figure', 'expr', 'choices', 'answer', 'explain', 'wrong_explain', 'concept')
    out = {'id': new_id, 'part': part}
    for k in keep:
        if k in it:
            out[k] = it[k]
    out['stem'] = strip_ref(out['stem'])
    out['src'] = ref
    out['topic'] = topic
    return out


def build(subject, cfg):
    mcq, fill = load_pool(subject)
    used = set()
    exams = []
    for n in range(1, cfg['exams'] + 1):
        rng = random.Random(f'{subject}-de-{n}')
        items = []
        # Phần I: 12 câu; khoảng 1/3 là mức Vận dụng, còn lại Biết và Hiểu; sắp từ dễ đến khó.
        chosen = []
        levels = ['Biết'] * 2 + ['Hiểu'] * 6 + ['Vận dụng'] * 4
        rng.shuffle(levels)
        slots = [ch for ch, k in cfg['p1'].items() for _ in range(k)]
        for ch, lv in zip(slots, levels):
            chosen.append(take(rng, mcq, ch, used, [lv, 'Hiểu', 'Biết', 'Vận dụng']))
        order = {'Biết': 0, 'Hiểu': 1, 'Vận dụng': 2, 'Nâng cao': 3}
        chosen.sort(key=lambda x: (order.get(x[0].get('level'), 1), rng.random()))
        for i, (it, ref, topic) in enumerate(chosen, 1):
            items.append(clean(it, f'p1q{i:02d}', 1, ref, topic))
        # Phần II: 4 câu đúng–sai từ câu trắc nghiệm mức Hiểu hoặc Vận dụng.
        for i, ch in enumerate(cfg['p2'], 1):
            it, ref, topic = take(rng, mcq, ch, used, ['Hiểu', 'Vận dụng', 'Biết'])
            sts = []
            for ci, text in enumerate(it['choices']):
                ok = ci == it['answer']
                sts.append({'text': text, 'truth': ok, 'explain': it['explain'] if ok else it['wrong_explain'][str(ci)]})
            rng.shuffle(sts)
            tf = {'id': f'p2q{i:02d}', 'part': 2, 'type': 'tf', 'level': it.get('level', 'Hiểu'), 'stem': strip_ref(it['stem']), 'statements': sts, 'src': ref, 'topic': topic}
            if 'figure' in it:
                tf['figure'] = it['figure']
            items.append(tf)
        # Phần III: 6 câu trả lời ngắn, ưu tiên mức Vận dụng.
        for i, ch in enumerate(cfg['p3'], 1):
            it, ref, topic = take(rng, fill, ch, used, ['Vận dụng', 'Hiểu', 'Biết'])
            items.append(clean(it, f'p3q{i:02d}', 3, ref, topic))
        exams.append({
            'id': f'de-{n:02d}', 'kind': 'exam', 'grade': 12, 'subject': subject.rstrip('0123456789'),
            'bookSeries': 'Nam Linh Educenter', 'book': 'Đề thi thử tốt nghiệp', 'chapter': 'Đề thi thử theo cấu trúc tốt nghiệp THPT',
            'lesson': f'Đề thi thử số {n}', 'title': f'Đề thi thử tốt nghiệp THPT số {n}', 'durationMin': 90,
            'structure': {'p1': {'n': 12, 'each': 0.25}, 'p2': {'n': 4, 'byCorrect': [0, 0.1, 0.25, 0.5, 1]}, 'p3': {'n': 6, 'each': 0.5}},
            'theory': [], 'items': items,
        })
    return exams


def main():
    for subject, cfg in CONFIG.items():
        exams = build(subject, cfg)
        d = os.path.join(CONTENT, subject, 'de-thi')
        os.makedirs(d, exist_ok=True)
        for e in exams:
            with open(os.path.join(d, e['id'] + '.json'), 'w', encoding='utf8') as fh:
                json.dump(e, fh, ensure_ascii=False, indent=2); fh.write('\n')
        mp = os.path.join(CONTENT, subject, 'manifest.json')
        m = json.load(open(mp, encoding='utf8'))
        m['books'] = [b for b in m['books'] if b['id'] != 'de-thi']
        m['books'].append({'id': 'de-thi', 'title': 'Đề thi thử tốt nghiệp', 'chapters': [{
            'id': 'de-thi', 'title': 'Đề thi thử theo cấu trúc tốt nghiệp THPT',
            'lessons': [{'id': e['id'], 'title': e['title'], 'file': f"de-thi/{e['id']}.json"} for e in exams]}]})
        with open(mp, 'w', encoding='utf8') as fh:
            json.dump(m, fh, ensure_ascii=False, indent=2); fh.write('\n')
        print(subject, len(exams), 'đề')


if __name__ == '__main__':
    main()
