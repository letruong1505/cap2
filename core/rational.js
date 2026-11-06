// Tính toán số hữu tỉ chính xác bằng số nguyên lớn (BigInt).
// Dùng chung cho giao diện (renderer) và bộ kiểm tra nội dung (tools).
// Hỗ trợ: số nguyên, phân số a/b, dấu âm, phép + - * /, ngoặc đơn.

(function (root) {
  function gcd(a, b) {
    a = a < 0n ? -a : a;
    b = b < 0n ? -b : b;
    while (b !== 0n) [a, b] = [b, a % b];
    return a;
  }

  function make(n, d) {
    if (d === 0n) throw new Error('Mẫu số bằng 0');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcd(n, d) || 1n;
    return { n: n / g, d: d / g };
  }

  const add = (x, y) => make(x.n * y.d + y.n * x.d, x.d * y.d);
  const sub = (x, y) => make(x.n * y.d - y.n * x.d, x.d * y.d);
  const mul = (x, y) => make(x.n * y.n, x.d * y.d);
  const div = (x, y) => {
    if (y.n === 0n) throw new Error('Chia cho 0');
    return make(x.n * y.d, x.d * y.n);
  };
  const equal = (x, y) => x.n === y.n && x.d === y.d;

  // Đọc chuỗi như "-3/4", "5", "(-7/10)". Không chấp nhận chuỗi rỗng hay ký tự lạ.
  function parse(str) {
    const s = String(str).replace(/\s+/g, '');
    if (s === '') throw new Error('Chuỗi rỗng');
    let pos = 0;

    function peek() { return s[pos]; }

    function parseNumber() {
      const m = /^\d+/.exec(s.slice(pos));
      if (!m) throw new Error('Không đọc được số tại vị trí ' + pos);
      pos += m[0].length;
      let n = BigInt(m[0]);
      let d = 1n;
      if (peek() === '/') {
        pos += 1;
        const m2 = /^\d+/.exec(s.slice(pos));
        if (!m2) throw new Error('Thiếu mẫu số');
        pos += m2[0].length;
        d = BigInt(m2[0]);
      }
      return make(n, d);
    }

    function parseFactor() {
      if (peek() === '-') { pos += 1; const v = parseFactor(); return make(-v.n, v.d); }
      if (peek() === '+') { pos += 1; return parseFactor(); }
      if (peek() === '(') {
        pos += 1;
        const v = parseExpr();
        if (peek() !== ')') throw new Error('Thiếu dấu ngoặc đóng');
        pos += 1;
        return v;
      }
      return parseNumber();
    }

    function parseTerm() {
      let v = parseFactor();
      while (peek() === '*' || peek() === '/') {
        const op = s[pos];
        pos += 1;
        const r = parseFactor();
        v = op === '*' ? mul(v, r) : div(v, r);
      }
      return v;
    }

    function parseExpr() {
      let v = parseTerm();
      while (peek() === '+' || peek() === '-') {
        const op = s[pos];
        pos += 1;
        const r = parseTerm();
        v = op === '+' ? add(v, r) : sub(v, r);
      }
      return v;
    }

    const value = parseExpr();
    if (pos !== s.length) throw new Error('Thừa ký tự tại vị trí ' + pos);
    return value;
  }

  // Tính giá trị một biểu thức, ví dụ "2/5 + (-7/10) - 1/2".
  const evaluate = (expr) => parse(expr);

  // So hai chuỗi số/biểu thức theo giá trị (1/2 bằng 2/4). Trả về false nếu một vế không đọc được.
  function sameValue(a, b) {
    try {
      return equal(parse(a), parse(b));
    } catch {
      return false;
    }
  }

  const api = { parse, evaluate, equal, sameValue, add, sub, mul, div };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    root.Rational = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
