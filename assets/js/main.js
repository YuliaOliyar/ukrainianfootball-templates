// Футбол України — мінімальний JS шаблонів (без залежностей)
(function () {
  // Мобільне меню
  var btn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Закрити' : 'Меню';
    });
  }
  // Підменю: кнопка-стрілка відкриває/закриває (на мобільному — акордеон), Esc і клік поза меню закривають
  var subs = document.querySelectorAll('.menu .has-sub');
  function closeAll(except) {
    subs.forEach(function (li) {
      if (li === except) return;
      li.classList.remove('is-open');
      var b = li.querySelector('.sub-toggle'); if (b) b.setAttribute('aria-expanded', 'false');
    });
  }
  subs.forEach(function (li) {
    var b = li.querySelector('.sub-toggle');
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !li.classList.contains('is-open');
      closeAll(li);
      li.classList.toggle('is-open', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.menu')) closeAll(); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var li = document.activeElement && document.activeElement.closest('.has-sub');
    closeAll();
    if (li) { li.querySelector('.sub-toggle').focus(); li.querySelector('.sub-toggle').blur(); }
    if (document.activeElement) document.activeElement.blur();
  });
  // Календар: прокрутити смугу турів до поточного туру
  var cur = document.querySelector('.rounds .is-current');
  if (cur && cur.scrollIntoView) {
    var strip = cur.closest('.rounds');
    strip.scrollLeft = cur.offsetLeft - strip.clientWidth / 2 + cur.clientWidth / 2;
  }
})();
// Трансфери: фільтр таблиці переходів за клубом
(function () {
  var sel = document.getElementById('club-filter');
  var rows = document.querySelectorAll('table.transfers tbody tr');
  if (!sel || !rows.length) return;
  var empty = document.querySelector('.tempty');
  sel.addEventListener('change', function () {
    var c = sel.value, shown = 0;
    rows.forEach(function (r) {
      var ok = !c || r.dataset.from === c || r.dataset.to === c;
      r.hidden = !ok; if (ok) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  });
})();
// Гравці: фільтр складів за клубом
(function () {
  var sel = document.getElementById('club-filter');
  var rows = document.querySelectorAll('table.players tbody tr');
  if (!sel || !rows.length) return;
  var empty = document.querySelector('.tempty');
  sel.addEventListener('change', function () {
    var c = sel.value, shown = 0;
    rows.forEach(function (r) { var ok = !c || r.dataset.club === c; r.hidden = !ok; if (ok) shown++; });
    if (empty) empty.hidden = shown > 0;
  });
})();
// Матч-центр: фільтр «Усі / Наживо / Завершені / Попереду»
(function () {
  var chips = document.querySelectorAll('.chips .chip');
  if (!chips.length) return;
  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.dataset.f;
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.matches--live > li').forEach(function (li) { li.hidden = !!f && li.dataset.state !== f; });
      document.querySelectorAll('.matches--live').forEach(function (ul) {
        var p = ul.closest('.panel'); if (p) p.hidden = !ul.querySelector('li:not([hidden])');
      });
    });
  });
})();
