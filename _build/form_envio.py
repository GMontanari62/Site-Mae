# -*- coding: utf-8 -*-
"""Patch unico (ja aplicado): envio do formulario por fetch com animacao de sucesso e aviso de erro. Nao rodar de novo."""
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rw(p, f):
    p = os.path.join(ROOT, p)
    s = io.open(p, encoding="utf8", newline="").read()
    n = f(s)
    assert n != s, p
    io.open(p, "w", encoding="utf8", newline="").write(n)

html_err = '''      <div class="fe" id="fe" hidden role="alert" tabindex="-1">
        <svg class="fe-ic" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 7v6M12 16.5v.1"/></svg>
        <div class="fe-tx"><strong>Não foi possível enviar</strong><span id="feMsg">Tente novamente em instantes ou fale com a gente pelo WhatsApp.</span></div>
        <a class="btn btn-wa" href="https://wa.me/5531988660712?text=Ol%C3%A1%2C%20gostaria%20de%20solicitar%20um%20or%C3%A7amento." target="_blank" rel="noopener">Chamar no WhatsApp</a>
      </div>
      <button class="btn btn-primary" type="submit">Enviar pedido</button>'''

html_ok = '''    <div class="fs" id="fs" hidden role="status" aria-live="polite" tabindex="-1">
        <div class="fs-ck" aria-hidden="true">
          <svg viewBox="0 0 52 52" width="96" height="96"><circle class="fs-c" cx="26" cy="26" r="24"/><path class="fs-t" d="M14.5 27.5l8 8 15-17"/></svg>
          <span class="fs-ring"></span>
          <i style="--a:0deg"></i><i style="--a:36deg"></i><i style="--a:72deg"></i><i style="--a:108deg"></i><i style="--a:144deg"></i><i style="--a:180deg"></i><i style="--a:216deg"></i><i style="--a:252deg"></i><i style="--a:288deg"></i><i style="--a:324deg"></i>
        </div>
        <strong class="fs-h">Pedido enviado com sucesso!</strong>
        <p>Recebemos sua mensagem. Retornamos em até 48 horas, no e-mail que você informou.</p>
        <button type="button" class="btn btn-ghost" id="fsNovo">Enviar outro pedido</button>
      </div>
    </form>'''

js = '''/* ===== envio do formulário sem sair da página: animação de sucesso ou aviso de erro ===== */
(function(){
  var f = $('#orc'), btn = f.querySelector('button[type=submit]'), fs = $('#fs'), fe = $('#fe'), feMsg = $('#feMsg'), novo = $('#fsNovo');
  var rotulo = btn.textContent, busy = false, ENDPOINT = 'https://formsubmit.co/ajax/carla@cmgenge.com.br';
  var padrao = feMsg.textContent;
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
    if (!window.fetch || !window.FormData) return;          /* navegador antigo: envio normal da página */
    ev.preventDefault();
    if (busy) return;
    busy = true; fe.hidden = true; btn.disabled = true; btn.classList.add('loading'); btn.textContent = 'Enviando…';
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 45000);
    fetch(ENDPOINT, {method:'POST', body:new FormData(f), headers:{'Accept':'application/json'}, signal: ctrl ? ctrl.signal : undefined})
      .then(function(r){ return r.json().catch(function(){ return {}; }).then(function(j){ return {ok:r.ok, j:j}; }); })
      .then(function(x){ clearTimeout(to); if (x.ok && String(x.j.success) !== 'false') ok(); else erro(); })
      .catch(function(err){ clearTimeout(to); erro(err && err.name === 'AbortError' ? 'O envio demorou demais. Verifique sua conexão e tente de novo.' : 'Sem conexão com o servidor. Verifique sua internet e tente de novo.'); });
  });
  novo.addEventListener('click', function(){
    f.classList.remove('done'); fs.hidden = true;
    var p = f.querySelector('input[name=nome]'); if (p) p.focus();
  });
})();

/* ===== anexos'''

def h(s):
    s = s.replace('      <button class="btn btn-primary" type="submit">Enviar pedido</button>', html_err, 1)
    s = s.replace('style="text-decoration:underline">Política de Privacidade</a>.</p>\n    </form>',
                  'style="text-decoration:underline">Política de Privacidade</a>.</p>\n' + html_ok, 1)
    s = s.replace("/* ===== anexos", js, 1)
    return s
rw("index.html", h)

css = '''
/* ===== formulário: envio, sucesso e erro ===== */
.c-form{position:relative}
.c-form button[type=submit].loading{pointer-events:none;opacity:.85}
.c-form button[type=submit].loading::after{content:"";display:inline-block;width:16px;height:16px;margin-left:10px;vertical-align:-3px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:fsSpin .7s linear infinite}
@keyframes fsSpin{to{transform:rotate(360deg)}}
.c-form .fe{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;margin:16px 0 4px;padding:16px;border-radius:var(--radius);background:#fdecec;border:1px solid #e9a5a5;color:#5c1414}
.c-form .fe[hidden]{display:none}
.c-form .fe:focus{outline:none}
.c-form .fe-ic{flex:none;color:#b42318}
.c-form .fe-tx{flex:1 1 200px;display:flex;flex-direction:column;gap:2px;font-size:var(--t-sm)}
.c-form .fe-tx strong{font-size:1rem}
.c-form .fe.shake{animation:fsShake .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes fsShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-6px)}40%,60%{transform:translateX(6px)}}
.c-form.done>*:not(.fs){display:none}
.c-form .fs{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:12px;min-height:340px;padding:32px 16px}
.c-form .fs[hidden]{display:none}
.c-form .fs:focus{outline:none}
.c-form .fs-h{font-family:var(--f-head);font-size:1.5rem;font-weight:800;line-height:1.2;color:var(--navy)}
.c-form .fs p{max-width:32ch;color:var(--ink-soft)}
.fs-ck{position:relative;width:96px;height:96px;margin-bottom:8px}
.fs-ck svg{position:relative;z-index:1;overflow:visible}
.fs-c{fill:rgba(20,184,166,.12);stroke:var(--teal);stroke-width:2.4;stroke-dasharray:151;stroke-dashoffset:151;transform-origin:center;transform:rotate(-90deg)}
.fs-t{fill:none;stroke:var(--teal);stroke-width:3.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:46;stroke-dashoffset:46}
.fs-ring{position:absolute;inset:0;border-radius:50%;border:2px solid var(--teal-glow);opacity:0}
.fs-ck i{position:absolute;left:50%;top:50%;width:8px;height:8px;margin:-4px;border-radius:50%;background:var(--teal-glow);opacity:0}
.fs-ck i:nth-of-type(even){background:var(--navy);width:6px;height:6px;margin:-3px}
.fs.go .fs-c{animation:fsDraw .7s cubic-bezier(.65,0,.35,1) forwards}
.fs.go .fs-t{animation:fsDraw .45s .55s cubic-bezier(.65,0,.35,1) forwards}
.fs.go .fs-ck svg{animation:fsPop .5s .9s cubic-bezier(.34,1.56,.64,1)}
.fs.go .fs-ring{animation:fsRing .9s .85s ease-out}
.fs.go .fs-ck i{animation:fsBurst .9s .85s cubic-bezier(.2,.7,.3,1) forwards}
.fs.go .fs-h,.fs.go p,.fs.go .btn{opacity:0;animation:fsUp .6s cubic-bezier(.2,.7,.3,1) forwards}
.fs.go .fs-h{animation-delay:1s}.fs.go p{animation-delay:1.12s}.fs.go .btn{animation-delay:1.25s}
@keyframes fsDraw{to{stroke-dashoffset:0}}
@keyframes fsPop{50%{transform:scale(1.12)}}
@keyframes fsRing{0%{opacity:.8;transform:scale(1)}100%{opacity:0;transform:scale(1.7)}}
@keyframes fsBurst{0%{opacity:1;transform:rotate(var(--a)) translateY(-44px) scale(1)}100%{opacity:0;transform:rotate(var(--a)) translateY(-86px) scale(.4)}}
@keyframes fsUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  .fs.go .fs-c,.fs.go .fs-t{animation:none;stroke-dashoffset:0}
  .fs.go .fs-ck i,.fs.go .fs-ring{display:none}
  .fs.go .fs-ck svg,.fs.go .fs-h,.fs.go p,.fs.go .btn,.c-form .fe.shake{animation:none;opacity:1}
}
'''
rw("assets/css/fixes.css", lambda s: s + css)
print("ok")
