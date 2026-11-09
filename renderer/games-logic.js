// Logic thuần cho trò chơi: chọn câu hợp lệ, kiểm tra đáp án, ghép cặp, chuỗi ngày học.
// Không đụng tới DOM, nên kiểm thử được bằng node (tests/games.test.js).
// Mọi đáp án được so theo giá trị (R.sameValue), không theo chuỗi gõ vào.

(function (root) {
  const R = typeof module !== 'undefined' && module.exports
    ? require('../core/rational.js')
    : root.Rational;

  // Trộn Fisher–Yates, nhận rng để kiểm thử lặp lại được.
  function shuffle(arr, rng = Math.random) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // Số thập phân hiển thị kiểu Việt Nam: 4.5 thành 4,5.
  function viNumber(v) {
    const t = String(v);
    return /^-?\d+\.\d+$/.test(t) ? t.replace('.', ',') : t;
  }

  // Khoá so sánh theo giá trị: 2/4 và 1/2 cùng khoá.
  function valueKey(text) {
    const v = R.evaluate(String(text));
    return `${v.n}/${v.d}`;
  }

  // Câu chỉ đưa vào trò chơi khi đáp án kiểm được chắc chắn.
  // Câu có hình minh họa bị loại: hình có thể chứa thông tin cần thiết để giải.
  function isGameItem(item) {
    if (!item || item.figure || item.figureSvg) return false;
    if (item.type === 'mcq') {
      if (!Array.isArray(item.choices) || item.choices.length < 2) return false;
      if (!Number.isInteger(item.answer) || item.answer < 0 || item.answer >= item.choices.length) return false;
      const texts = item.choices.map((c) => String(c).trim());
      if (texts.some((t) => t === '') || new Set(texts).size !== texts.length) return false;
      if (item.expr) {
        try {
          if (!R.sameValue(item.expr, item.choices[item.answer])) return false;
        } catch {
          return false;
        }
        // Nếu một phương án khác cũng bằng biểu thức thì câu bị mơ hồ.
        const dup = item.choices.some((c, i) => i !== item.answer && R.sameValue(item.expr, c));
        if (dup) return false;
      }
      return true;
    }
    if (item.type === 'fill') {
      if (!item.expr) return false;
      try {
        R.evaluate(item.expr);
        R.parse(String(item.answer));
      } catch {
        return false;
      }
      return R.sameValue(item.expr, item.answer);
    }
    return false;
  }

  // Gom các câu hợp lệ từ danh sách bài đã mở (bỏ bài tự luận).
  function collectPool(lessons) {
    const pool = [];
    for (const lesson of lessons || []) {
      if (!lesson || lesson.kind === 'review' || !Array.isArray(lesson.items)) continue;
      for (const item of lesson.items) {
        if (isGameItem(item)) {
          pool.push({ ...item, lessonId: lesson.id, lessonTitle: lesson.lesson || lesson.title || '' });
        }
      }
    }
    return pool;
  }

  function pickQuestions(pool, n, rng = Math.random) {
    return shuffle(pool, rng).slice(0, Math.max(0, n));
  }

  // Kiểm tra một lựa chọn trắc nghiệm theo chỉ số phương án gốc.
  function isChoiceCorrect(item, choiceIndex) {
    return choiceIndex === item.answer;
  }

  // Kiểm tra câu điền: trả về { valid, correct }. Nhập sai định dạng thì không tính là đã trả lời.
  function checkFill(item, text) {
    const t = String(text ?? '').trim();
    if (t === '') return { valid: false, correct: false };
    try {
      R.parse(t);
    } catch {
      return { valid: false, correct: false };
    }
    return { valid: true, correct: R.sameValue(t, item.answer) };
  }

  // Cặp ghép: biểu thức bên trái, kết quả bên phải. Mỗi kết quả chỉ xuất hiện một lần.
  function buildPairs(pool, n, rng = Math.random) {
    const candidates = shuffle(pool.filter((i) => i.type === 'fill' && i.expr), rng);
    const seen = new Set();
    const pairs = [];
    for (const it of candidates) {
      const key = valueKey(it.answer);
      if (seen.has(key)) continue;
      seen.add(key);
      pairs.push({
        id: it.id,
        lessonId: it.lessonId,
        key,
        left: it.expr.replace(/\*/g, '×'),
        right: viNumber(it.answer),
        equation: `${it.expr.replace(/\*/g, '×')} = ${viNumber(it.answer)}`,
      });
      if (pairs.length === n) break;
    }
    return pairs;
  }

  // Chuỗi ngày học theo ngày địa phương (YYYY-MM-DD).
  function dayKey(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }

  function prevDayKey(key) {
    const [y, m, d] = key.split('-').map(Number);
    return dayKey(new Date(y, m - 1, d - 1));
  }

  function normalizeStreak(store) {
    const s = store || {};
    return {
      last: typeof s.last === 'string' ? s.last : null,
      count: Number.isInteger(s.count) && s.count > 0 ? s.count : 0,
      best: Number.isInteger(s.best) && s.best > 0 ? s.best : 0,
    };
  }

  // Ghi nhận một ngày học (nộp bài luyện tập). Cùng ngày thì không đếm lại.
  function recordStudy(store, date) {
    const s = normalizeStreak(store);
    const today = dayKey(date);
    if (s.last === today) return s;
    const count = s.last === prevDayKey(today) ? s.count + 1 : 1;
    return { last: today, count, best: Math.max(s.best, count) };
  }

  // Chuỗi hiện tại: đứt nếu bỏ qua cả hôm qua lẫn hôm nay.
  function currentStreak(store, date) {
    const s = normalizeStreak(store);
    const today = dayKey(date);
    if (s.last === today || s.last === prevDayKey(today)) return s.count;
    return 0;
  }

  const BADGES = [
    { days: 3, name: 'Khởi động' },
    { days: 7, name: 'Kiên trì' },
    { days: 14, name: 'Bền bỉ' },
    { days: 30, name: 'Thói quen' },
  ];

  function badgesFor(count) {
    return BADGES.map((b) => ({ ...b, earned: count >= b.days }));
  }

  // Điểm cao nhất theo từng trò chơi và môn. Trả về bản sao, không sửa đối tượng cũ.
  function updateBest(bests, gameId, subject, score) {
    const next = { ...(bests || {}) };
    const key = `${gameId}:${subject}`;
    const prev = Number.isInteger(next[key]) ? next[key] : null;
    if (prev === null || score > prev) next[key] = score;
    return next;
  }

  const api = {
    shuffle, viNumber, valueKey, isGameItem, collectPool, pickQuestions,
    isChoiceCorrect, checkFill, buildPairs,
    dayKey, normalizeStreak, recordStudy, currentStreak, badgesFor, BADGES, updateBest,
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    root.VungGamesLogic = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
