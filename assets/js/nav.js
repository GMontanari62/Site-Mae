/* Menu: botão do celular, dropdown de Serviços e submenus */
(function () {
  var b = document.getElementById('burger'), n = document.getElementById('nav'), hd = document.getElementById('top');
  var root = document.documentElement, mq = window.matchMedia('(max-width:768px)'), resetT = null;
  function resetAcc() {
    Array.prototype.forEach.call(document.querySelectorAll('.dd.open, .dd-s.open'), function (x) { x.classList.remove('open'); });
    var l = document.querySelector('.dd>a.lnk'); if (l) l.setAttribute('aria-expanded', 'false');
  }
  function setOpen(v) {
    n.classList.toggle('open', v);
    b.classList.toggle('is-open', v);
    b.setAttribute('aria-expanded', v ? 'true' : 'false');
    b.setAttribute('aria-label', v ? 'Fechar menu' : 'Abrir menu');
    root.classList.toggle('menu-open', v);
    if (hd) hd.classList.toggle('menu-open', v);
    clearTimeout(resetT);
    if (!v) resetT = setTimeout(resetAcc, 450);   /* fecha o acordeão só depois da animação de saída */
  }
  if (b && n) {
    b.addEventListener('click', function () { setOpen(!n.classList.contains('open')); });
    n.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) { if (e.target === n) setOpen(false); return; }
      if (mq.matches && a.matches('.dd>a.lnk')) {        /* Serviços no celular: abre/fecha o dropdown */
        e.preventDefault();
        var dd = a.parentElement, v = !dd.classList.contains('open');
        dd.classList.toggle('open', v);
        a.setAttribute('aria-expanded', v ? 'true' : 'false');
        return;
      }
      setOpen(false);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && n.classList.contains('open')) setOpen(false); });
    var onMq = function () { if (!mq.matches && n.classList.contains('open')) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onMq); else mq.addListener(onMq);
  }
  /* barra fina de progresso de leitura na base do cabeçalho */
  if (hd) {
    var tick = false;
    var prog = function () {
      tick = false;
      var t = root.scrollHeight - window.innerHeight;
      hd.style.setProperty('--sp', (t > 0 ? Math.min(100, window.pageYOffset / t * 100) : 0).toFixed(2) + '%');
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(prog); } }, { passive: true });
    prog();
  }
  var subs = Array.prototype.slice.call(document.querySelectorAll('.dd-s'));
  subs.forEach(function (s) {
    var t = s.querySelector('button.dd-t');
    if (!t) return;
    t.addEventListener('click', function () {
      var open = !s.classList.contains('open');
      subs.forEach(function (o) { o.classList.remove('open'); var bt = o.querySelector('button.dd-t'); if (bt) bt.setAttribute('aria-expanded', 'false'); });
      if (open) { s.classList.add('open'); t.setAttribute('aria-expanded', 'true'); }
    });
    /* abre para o lado oposto se o submenu não couber na tela */
    s.addEventListener('mouseenter', function () {
      s.classList.remove('flip');
      var r = s.getBoundingClientRect();
      if (r.right + 10 + 340 > window.innerWidth - 8) s.classList.add('flip');
    });
  });
  var dd = document.querySelector('.dd');
  if (dd) {
    dd.addEventListener('mouseleave', function () { subs.forEach(function (o) { o.classList.remove('open'); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { subs.forEach(function (o) { o.classList.remove('open'); }); if (document.activeElement) document.activeElement.blur(); }
    });
  }
})();

/* Âncoras: centraliza a seção na área visível abaixo do cabeçalho fixo.
   Se a seção for mais alta que a tela, alinha o topo dela logo abaixo do cabeçalho. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function targetTop(el) {
    var head = document.getElementById('top'), h = head ? head.offsetHeight : 0;
    if (el.id === 'inicio') return 0;
    var r = el.getBoundingClientRect(), avail = window.innerHeight - h;
    var y = window.pageYOffset + r.top - h;
    if (r.height < avail) y -= (avail - r.height) / 2;
    return Math.max(0, Math.round(y));
  }
  function go(el, smooth) {
    window.scrollTo({ top: targetTop(el), behavior: (smooth && !reduce) ? 'smooth' : 'instant' });
  }
  function fromHash(smooth) {
    var id = decodeURIComponent((location.hash || '').slice(1));
    var el = id && document.getElementById(id);
    if (el) go(el, smooth);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href').length < 2) return;
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (!el) return;
    e.preventDefault();
    if (history.pushState) history.pushState(null, '', a.getAttribute('href'));
    go(el, true);
  });
  window.addEventListener('hashchange', function () { fromHash(true); });
  /* chegada por link de outra página (index.html#sobre): ajusta depois do carregamento */
  window.addEventListener('load', function () { if (location.hash) setTimeout(function () { fromHash(false); }, 60); });
})();
