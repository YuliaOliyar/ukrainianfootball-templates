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
