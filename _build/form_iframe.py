# -*- coding: utf-8 -*-
"""Patch unico (ja aplicado): troca o envio por fetch/AJAX (que travava) pelo envio normal do FormSubmit dentro de um iframe invisivel,
com redirecionamento (_next) para /enviado.html, que e do mesmo site e por isso pode ser lido para saber que deu certo. Nao rodar de novo."""
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "index.html")
s = io.open(p, encoding="utf8", newline="").read()
a = s.index("/* ===== envio do formulário sem sair da página")
b = s.index("/* ===== anexos")
novo = '''/* ===== envio do formulário sem sair da página: animação de sucesso ou aviso de erro =====
   O envio é o normal do FormSubmit (aceita anexos), feito dentro de um quadro invisível. Quando dá certo, o FormSubmit
   redireciona o quadro para /enviado.html (do mesmo site), e é isso que confirma o sucesso. Qualquer outra página = erro. */
(function(){
  var f = $('#orc'), btn = f.querySelector('button[type=submit]'), fs = $('#fs'), fe = $('#fe'), feMsg = $('#feMsg'), novo = $('#fsNovo');
  var rotulo = btn.textContent, padrao = feMsg.textContent, busy = false, to = null;
  var fr = document.createElement('iframe');
  fr.name = 'fsframe'; fr.title = 'Envio do formulário'; fr.hidden = true; fr.tabIndex = -1; fr.setAttribute('aria-hidden', 'true');
  document.body.appendChild(fr);
  var nx = document.createElement('input');
  nx.type = 'hidden'; nx.name = '_next'; nx.value = location.origin + '/enviado.html'; f.appendChild(nx);
  function volta(){ busy = false; clearTimeout(to); btn.disabled = false; btn.classList.remove('loading'); btn.textContent = rotulo; f.removeAttribute('target'); }
  function erro(msg){
    volta();
    feMsg.textContent = msg || padrao;
    fe.hidden = false; fe.classList.remove('shake'); void fe.offsetWidth; fe.classList.add('shake');
    fe.scrollIntoView({block:'center', behavior:'smooth'}); fe.focus({preventScroll:true});
  }
  function ok(){
    volta(); f.reset(); fe.hidden = true;
    f.classList.add('done'); fs.hidden = false;
    fs.classList.remove('go'); void fs.offsetWidth; fs.classList.add('go');
    f.scrollIntoView({block:'start', behavior:'smooth'}); fs.focus({preventScroll:true});
  }
  fr.addEventListener('load', function(){
    if (!busy) return;                                       /* carga inicial do quadro vazio */
    var certo = false;
    try { certo = fr.contentWindow.location.pathname.indexOf('enviado') > -1; } catch (e) { certo = false; }   /* página de outro site = não confirmou */
    if (certo) ok(); else erro();
  });
  f.addEventListener('submit', function(ev){
    if (busy){ ev.preventDefault(); return; }
    busy = true; fe.hidden = true; btn.disabled = true; btn.classList.add('loading'); btn.textContent = 'Enviando…';
    f.target = 'fsframe';
    to = setTimeout(function(){ if (busy) erro('O envio demorou demais. Verifique sua conexão e tente de novo.'); }, 90000);
  });
  novo.addEventListener('click', function(){
    f.classList.remove('done'); fs.hidden = true;
    var p = f.querySelector('input[name=nome]'); if (p) p.focus();
  });
})();

'''
s = s[:a] + novo + s[b:]
io.open(p, "w", encoding="utf8", newline="").write(s)

# pagina de confirmacao (so serve de destino do redirecionamento; nao aparece nos buscadores)
io.open(os.path.join(ROOT, "enviado.html"), "w", encoding="utf8", newline="").write(
    '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
    '<title>Pedido enviado | CMG Engenharia</title></head><body><p>Pedido enviado. <a href="/">Voltar ao site</a></p></body></html>\n')

mp = os.path.join(ROOT, "_build", "make_deploy.py")
m = io.open(mp, encoding="utf8", newline="").read()
m = m.replace('"assets/video/hero-m.mp4"', '"enviado.html", "assets/video/hero-m.mp4"', 1)
io.open(mp, "w", encoding="utf8", newline="").write(m)
print("ok")
