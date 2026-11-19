// Đọc nội dung bài học đóng gói trong app (thư mục content/ cạnh index.html). Cùng quy tắc với main/content-loader.js.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileContent = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function safeRel(rel) {
    if (typeof rel !== 'string' || !rel || rel.indexOf('..') >= 0 || rel.charAt(0) === '/' || rel.indexOf('\\') >= 0 || rel.indexOf(':') >= 0) throw new Error('Đường dẫn nội dung không hợp lệ');
    return rel;
  }

  function checkLesson(lesson, relPath) {
    var problems = [];
    if (!lesson.id) problems.push('thiếu id');
    if (lesson.kind === 'review') {
      if (!Array.isArray(lesson.questions)) problems.push('thiếu danh sách câu tự luận');
    } else {
      if (!Array.isArray(lesson.items)) problems.push('thiếu danh sách câu hỏi');
      if (!Array.isArray(lesson.theory)) problems.push('thiếu lý thuyết');
    }
    if (problems.length) throw new Error('Bài ' + relPath + ' không hợp lệ: ' + problems.join(', '));
    return lesson;
  }

  // o.fetchText(url) -> Promise<string>; o.subjects: danh sách môn được phép; o.base: tiền tố thư mục nội dung.
  function create(o) {
    var base = o.base || 'content/';
    var subjects = o.subjects;
    function assertSubject(subject) { if (subjects.indexOf(subject) < 0) throw new Error('Môn học không hợp lệ'); return subject; }
    function readJson(rel) { return o.fetchText(base + safeRel(rel)).then(JSON.parse); }

    function attachFigures(lesson, subject) {
      var jobs = [];
      var read = function (obj, key, outKey) { jobs.push(o.fetchText(base + safeRel(subject + '/' + obj[key])).then(function (svg) { obj[outKey] = svg; })); };
      (lesson.items || []).forEach(function (i) { if (i.figure) read(i, 'figure', 'figureSvg'); });
      (lesson.questions || []).forEach(function (q) { if (q.figure) read(q, 'figure', 'figureSvg'); });
      (lesson.theory || []).forEach(function (b) { if (b.type === 'figure') read(b, 'figure', 'figureSvg'); });
      (lesson.examples || []).forEach(function (e) { if (e.figure) read(e, 'figure', 'figureSvg'); });
      return Promise.all(jobs).then(function () { return lesson; });
    }

    return {
      loadManifest: function (subject) { return Promise.resolve().then(function () { return readJson(assertSubject(subject) + '/manifest.json'); }); },
      loadLesson: function (relPath) {
        return Promise.resolve().then(function () {
          var subject = assertSubject(String(relPath).split('/')[0]);
          return readJson(relPath).then(function (l) { return attachFigures(checkLesson(l, relPath), subject); });
        });
      },
    };
  }
  return { create: create, safeRel: safeRel };
});
