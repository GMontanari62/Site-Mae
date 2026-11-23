# -*- coding: utf-8 -*-
"""Pagina Servicos no celular: botao Filtrar + carrossel por grupo. Rodar uma vez; depois build.py."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
bp = os.path.join(HERE, "build.py")
b = open(bp, encoding="utf8").read()
assert 'id="fltBtn"' not in b, "patch5 ja aplicado"

# 1) botao Filtrar (some no desktop por CSS), antes da dica de hover
FLT = ('<div class="flt" id="flt"><button type="button" class="flt-btn" id="fltBtn" aria-expanded="false" aria-controls="fltPanel">'
       '<svg class="flt-i" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h9M19 7h1M4 17h1M11 17h9"/><circle cx="16" cy="7" r="2.2"/><circle cx="8" cy="17" r="2.2"/></svg>'
       '<span class="flt-l">Filtrar</span><span class="flt-v" id="fltV">Todos</span>'
       '<svg class="flt-c" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>'
       '<div class="flt-p" id="fltPanel" role="listbox" aria-label="Filtrar serviços"><div class="flt-in">'
       '<button type="button" class="flt-o" role="option" data-t="all" aria-selected="true"><span>Todos</span><small>10</small></button>'
       '<button type="button" class="flt-o" role="option" data-t="projetos" aria-selected="false"><span>Projetos Complementares</span><small>3</small></button>'
       '<button type="button" class="flt-o" role="option" data-t="vistoria" aria-selected="false"><span>Vistoria e Perícia</span><small>6</small></button>'
       '<button type="button" class="flt-o" role="option" data-t="social" aria-selected="false"><span>Engenharia Social</span><small>1</small></button>'
       '</div></div></div>\n')
old = '<p class="svc-hint" aria-hidden="true">'
assert old in b
b = b.replace(old, FLT + old, 1)

# 2) grupos com um servico so nao viram carrossel
old = "return '<div class=\"scards\">' + ''.join(scard(x, \"\") for x in lst) + '</div>'"
assert old in b
b = b.replace(old, "return '<div class=\"scards' + (' one' if len(lst) == 1 else '') + '\">' + ''.join(scard(x, \"\") for x in lst) + '</div>'", 1)

# 3) script: abas + painel Filtrar + pontinhos dos carrosseis
i = b.index('parts.append("""<script>\n(function(){\n  var tabs=')
j = b.index('</script>""")', i) + len('</script>""")')
NEWJS = r'''parts.append("""<script>
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tab')),opts=[].slice.call(document.querySelectorAll('.flt-o')),grps=[].slice.call(document.querySelectorAll('.sgrp'));
  var flt=document.getElementById('flt'),btn=document.getElementById('fltBtn'),val=document.getElementById('fltV');
  var names={all:'Todos',projetos:'Projetos Complementares',vistoria:'Vistoria e Perícia',social:'Engenharia Social'};
  function setFlt(v){if(!flt)return;flt.classList.toggle('open',v);btn.setAttribute('aria-expanded',v?'true':'false');}
  function show(t){
    tabs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===t?'true':'false');});
    opts.forEach(function(o){o.setAttribute('aria-selected',o.dataset.t===t?'true':'false');});
    if(val)val.textContent=names[t];
    grps.forEach(function(g){
      var on=(t==='all'||g.dataset.g===t);
      if(on){g.hidden=false;requestAnimationFrame(function(){g.classList.remove('out');});}
      else{g.hidden=true;g.classList.add('out');}
    });
    if(history.replaceState)history.replaceState(null,'',t==='all'?location.pathname:'#'+t);
    setFlt(false);
  }
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});
  opts.forEach(function(o){o.addEventListener('click',function(){show(o.dataset.t);});});
  if(btn){
    btn.addEventListener('click',function(){setFlt(!flt.classList.contains('open'));});
    document.addEventListener('click',function(e){if(!flt.contains(e.target))setFlt(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')setFlt(false);});
  }
  /* pontinhos dos carrosseis (só aparecem no celular) */
  [].slice.call(document.querySelectorAll('.sgrp .scards')).forEach(function(c){
    var n=c.children.length;if(n<2)return;
    var d=document.createElement('div');d.className='dots';
    for(var i=0;i<n;i++)d.appendChild(document.createElement('i'));
    c.parentNode.insertBefore(d,c.nextSibling);
    function upd(){
      var w=c.children[0].offsetWidth+12;
      var i=(c.scrollLeft+c.clientWidth>=c.scrollWidth-4)?n-1:Math.round(c.scrollLeft/Math.max(1,w));
      [].forEach.call(d.children,function(x,k){x.classList.toggle('on',k===i);});
    }
    c.addEventListener('scroll',function(){requestAnimationFrame(upd);},{passive:true});
    window.addEventListener('resize',upd);
    upd();
  });
  var h=location.hash.slice(1);
  if(names[h])show(h);
})();
</script>""")'''
b = b[:i] + NEWJS + b[j:]
open(bp, "w", encoding="utf8").write(b)
print("patch5 aplicado")
