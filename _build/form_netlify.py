# -*- coding: utf-8 -*-
"""Patch unico (ja aplicado): formulario passa do FormSubmit para o Netlify Forms (envio por fetch para o proprio site). Nao rodar de novo."""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "index.html")
s = io.open(p, encoding="utf8", newline="").read()

# 1) tag do formulario + campos ocultos
a = s.index('<form class="rv c-form" id="orc"')
b = s.index('<div class="row">', a)
novo_cab = '''<form class="rv c-form" id="orc" name="orcamento" action="/enviado.html" method="POST" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field">
      <h3>Solicitar orçamento</h3>
      <input type="hidden" name="form-name" value="orcamento">
      <input class="hp" type="text" name="bot-field" tabindex="-1" autocomplete="off" aria-hidden="true">
      '''
s = s[:a] + novo_cab + s[b:]

# 2) script de envio
a = s.index("/* ===== envio do formulário sem sair da página")
b = s.index("/* ===== anexos")
js = '''/* ===== envio do formulário (Netlify Forms) sem sair da página: animação de sucesso ou aviso de erro ===== */
(function(){
  var f = $('#orc'), btn = f.querySelector('button[type=submit]'), fs = $('#fs'), fe = $('#fe'), feMsg = $('#feMsg'), novo = $('#fsNovo');
  var rotulo = btn.textContent, padrao = feMsg.textContent, busy = false;
  function volta(){ busy = false; btn.disabled = false; btn.classList.remove('loading'); btn.textContent = rotulo; }
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
  f.addEventListener('submit', function(ev){
    if (!window.fetch || !window.FormData) return;          /* navegador antigo: envio normal da página (volta para /enviado.html) */
    ev.preventDefault();
    if (busy) return;
    busy = true; fe.hidden = true; btn.disabled = true; btn.classList.add('loading'); btn.textContent = 'Enviando…';
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 40000);
    /* sem Content-Type: o navegador monta o multipart com os anexos */
    fetch('/', {method:'POST', body:new FormData(f), signal: ctrl ? ctrl.signal : undefined})
      .then(function(r){ clearTimeout(to); if (r.ok) ok(); else erro(); })
      .catch(function(err){ clearTimeout(to); erro(err && err.name === 'AbortError' ? 'O envio demorou demais. Verifique sua conexão e tente de novo.' : 'Sem conexão com o servidor. Verifique sua internet e tente de novo.'); });
  });
  novo.addEventListener('click', function(){
    f.classList.remove('done'); fs.hidden = true;
    var p = f.querySelector('input[name=nome]'); if (p) p.focus();
  });
})();

'''
s = s[:a] + js + s[b:]
io.open(p, "w", encoding="utf8", newline="").write(s)

# pagina de confirmacao: agora e o destino do envio sem JavaScript, entao ganha mensagem de verdade
io.open(os.path.join(ROOT, "enviado.html"), "w", encoding="utf8", newline="").write(
    '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    '<meta name="robots" content="noindex"><meta name="color-scheme" content="only light"><title>Pedido enviado | CMG Engenharia</title>'
    '<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f5f5f5;color:#0e1c2e;font-family:Inter,Segoe UI,Arial,sans-serif;text-align:center;padding:24px}'
    'h1{font-size:1.6rem;margin:0 0 8px}p{margin:0 0 20px;color:#444}a{display:inline-block;padding:12px 24px;border-radius:999px;background:#087A74;color:#fff;text-decoration:none;font-weight:600}</style></head>'
    '<body><main><h1>Pedido enviado com sucesso!</h1><p>Recebemos sua mensagem. Retornamos em até 48 horas.</p><a href="/">Voltar ao site</a></main></body></html>\n')
print("ok")
