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
  if (!sel) return;
  var rows = document.querySelectorAll('table.transfers tbody tr');
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
