/* Ferramenta de teste (NÃO vai para a hospedagem). Carregue com fetch+eval e chame:
   await __audit('index.html', 375, 812)  ->  resumo de problemas daquela página nesse tamanho de tela. */
window.__audit = async function (url, W, H) {
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var f = document.createElement('iframe');
  f.style.cssText = 'position:fixed;left:-99999px;top:0;width:' + W + 'px;height:' + H + 'px;border:0';
  f.src = url; document.body.appendChild(f);
  await new Promise(function (r) { f.onload = r; });
  await sleep(600);
  [].slice.call(f.contentDocument.images).forEach(function (im) { if (!im.complete) im.loading = 'eager'; });   // imagens preguiçosas passam a carregar
  await sleep(1500);
  var w = f.contentWindow, d = f.contentDocument, root = d.documentElement, lw = root.clientWidth;
  var out = { pagina: url.replace('servicos/', 's/'), W: W, H: H, achados: {} };
  var add = function (k, v) { (out.achados[k] = out.achados[k] || []).push(v); };
  var sel = function (e) { return e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : ''); };
  var cs = function (e) { return w.getComputedStyle(e); };
  var inScroller = function (e) { for (var p = e.parentElement; p && p !== d.body; p = p.parentElement) { var o = cs(p).overflowX; if (o === 'auto' || o === 'scroll') return true; } return false; };
  var visible = function (e) {
    var s = cs(e); if (s.display === 'none' || s.visibility === 'hidden') return false;
    var r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0;
  };
  var skipSel = '.stage, .stage *, nav.main, nav.main *, .dd-p, .dd-p *, .sc-d, .hp, .sr-only, svg *, iframe, .loader-bar, #loader, #loader *';
  var all = [].slice.call(d.querySelectorAll('body *')).filter(function (e) { return !e.matches(skipSel) && visible(e); });

  // 1) estouro lateral da página
  if (root.scrollWidth > lw + 1) add('estouro-lateral', 'página ' + root.scrollWidth + 'px > tela ' + lw + 'px');

  // 2) elementos que passam da borda da tela (fora de carrosséis/roláveis)
  all.forEach(function (e) {
    if (inScroller(e)) return;
    var r = e.getBoundingClientRect();
    if (r.right > lw + 1.5 || r.left < -1.5) add('fora-da-tela', sel(e) + ' [' + Math.round(r.left) + '→' + Math.round(r.right) + ']');
  });

  // 3) texto cortado por overflow
  all.forEach(function (e) {
    var s = cs(e);
    if (s.overflowX === 'hidden' || s.overflowX === 'clip') {
      if (e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0 && (e.textContent || '').trim().length > 0 && !inScroller(e))
        add('texto-cortado-lateral', sel(e) + ' ' + e.scrollWidth + '>' + e.clientWidth);
    }
    if (s.textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth + 1) add('texto-com-reticencias', sel(e));
  });

  // 4) tamanho de texto
  var small = {};
  all.forEach(function (e) {
    var own = [].slice.call(e.childNodes).filter(function (n) { return n.nodeType === 3 && n.textContent.trim().length > 1; });
    if (!own.length) return;
    var fs = parseFloat(cs(e).fontSize);
    if (fs < 12) { var k = sel(e); small[k] = small[k] || { n: 0, fs: fs }; small[k].n++; small[k].fs = Math.min(small[k].fs, fs); }
  });
  Object.keys(small).forEach(function (k) { add('texto<12px', k + ' (' + small[k].fs.toFixed(1) + 'px ×' + small[k].n + ')'); });

  // 5) imagens
  [].slice.call(d.images).forEach(function (im) {
    var r = im.getBoundingClientRect(); if (!(r.width > 0)) return;
    if (!im.complete || im.naturalWidth === 0) { add('imagem-quebrada', im.getAttribute('src')); return; }
    if (r.width > im.naturalWidth * 1.05) add('imagem-ampliada(borrada)', im.getAttribute('src').split('/').pop() + ' ' + Math.round(r.width) + 'px sobre ' + im.naturalWidth + 'px');
  });

  // 6) alvos de toque pequenos (telas até 1024)
  if (W <= 1024) {
    var tgt = '.btn, button, .lnk, .tab, summary, .flt-o, .pn-tabs button, .c-tabs button, nav a, .scard, .card, .dd-t, input, select';
    [].slice.call(d.querySelectorAll(tgt)).filter(visible).forEach(function (e) {
      if (e.closest(skipSel.replace('.stage, .stage *, ', '').replace('nav.main, nav.main *, ', ''))) return;
      var r = e.getBoundingClientRect();
      if (Math.min(r.width, r.height) < 32 && e.type !== 'hidden') add('alvo-de-toque<32px', sel(e) + ' ' + Math.round(r.width) + '×' + Math.round(r.height));
    });
  }

  // 7) contraste de texto
  var parse = function (c) { var m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; var p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  var lum = function (c) { var f = function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  var bgOf = function (e) {
    for (var p = e; p && p.nodeType === 1; p = p.parentElement) {
      var s = cs(p);
      if (s.backgroundImage !== 'none') return null;           // gradiente/imagem: não dá para medir
      var c = parse(s.backgroundColor); if (c && c.a > 0.8) return c;
    }
    return { r: 245, g: 245, b: 245, a: 1 };
  };
  var seen = {};
  all.forEach(function (e) {
    var own = [].slice.call(e.childNodes).some(function (n) { return n.nodeType === 3 && n.textContent.trim().length > 1; });
    if (!own) return;
    var fg = parse(cs(e).color), bg = bgOf(e); if (!fg || !bg) return;
    if (e.closest('.sc-d, .hero, .scene2, .box, .layers')) return;
    var op = 1; for (var p = e; p && p.nodeType === 1; p = p.parentElement) op *= parseFloat(cs(p).opacity); if (op < 0.9) return;
    var a = fg.a; var mix = { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a) };
    var l1 = lum(mix), l2 = lum(bg), ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    var fs = parseFloat(cs(e).fontSize), bold = parseInt(cs(e).fontWeight) >= 700, large = fs >= 24 || (fs >= 18.66 && bold);
    if (ratio < (large ? 3 : 4.5)) { var k = sel(e); if (!seen[k]) { seen[k] = 1; add('contraste-baixo', k + ' ' + ratio.toFixed(1) + ':1 (' + fs.toFixed(0) + 'px)'); } }
  });

  f.remove();
  // resumo: conta e mantém os 3 primeiros exemplos
  var res = {}; Object.keys(out.achados).forEach(function (k) { var a = Array.from(new Set(out.achados[k])); res[k] = a.length + ' → ' + a.slice(0, 3).join(' | '); });
  out.achados = res; return out;
};
