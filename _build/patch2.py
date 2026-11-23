# -*- coding: utf-8 -*-
"""Aplica (uma vez) o dropdown, a pagina de servicos com imagens e as imagens por servico.
Rodar: python -I _build/patch2.py   (depois: python -I _build/build.py)"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from common import nav_html

# ============ build.py ============
bp = os.path.join(HERE, "build.py")
b = open(bp, encoding="utf8").read()
assert "from common import nav_html" not in b, "patch2 ja aplicado"

b = b.replace("import os, re, html, urllib.parse",
              "import os, re, sys, html, urllib.parse\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom common import nav_html", 1)

# nav do cabecalho
b, n = re.subn(r'<nav class="main" id="nav">.*?</nav>', '<nav class="main" id="nav">{nav_html(R)}</nav>', b, count=1, flags=re.S)
assert n == 1

# script do menu
old_js = "<script>\nvar b=document.getElementById('burger'),n=document.getElementById('nav');\nb.addEventListener('click',function(){{n.classList.toggle('open');}});\n</script>"
assert old_js in b
b = b.replace(old_js, '<script src="{R}assets/js/nav.js"></script>')

# imagens por servico + cartao com imagem
marker = 'BY_SLUG = {s["slug"]: s for s in S}'
assert marker in b
b = b.replace(marker, marker + '''
IMG = {
    "estrutura-concreto-alvenaria": ("projeto.webp", "Prancheta de engenharia com projeto estrutural, régua e capacete"),
    "instalacoes-hidrossanitarias": ("s-hidrossanitarias.webp", "Instalação hidrossanitária com tubulações de água e esgoto organizadas"),
    "instalacoes-eletricas-baixa-tensao": ("s-eletricas.webp", "Quadro de distribuição elétrica aberto, com disjuntores e cabos organizados"),
    "vistoria-de-reforma": ("s-reforma.webp", "Engenheiro avaliando uma parede em reforma de apartamento"),
    "vistoria-cautelar": ("cautelar.webp", "Casa vizinha a uma obra em construção, com linha técnica de medição"),
    "vistoria-de-entrega-de-imovel": ("s-entrega.webp", "Técnico conferindo a esquadria de um apartamento novo na entrega das chaves"),
    "vistoria-nbr-15575": ("s-desempenho.webp", "Técnico com câmera térmica avaliando o desempenho de um edifício residencial"),
    "inspecao-predial": ("inspecao.webp", "Técnico com capacete inspecionando a fachada de um edifício"),
    "pericia-estrutural": ("s-pericia.webp", "Pilar de concreto com fissura e armadura exposta e corroída"),
    "engenharia-social": ("social.webp", "Família diante de sua casa em reforma, com uma planta de engenharia em primeiro plano"),
}
for _k, _v in IMG.items():
    BY_SLUG[_k]["img"] = _v''', 1)

marker2 = "e = html.escape"
assert marker2 in b
b = b.replace(marker2, marker2 + '''

def scard(s, R):
    f, alt = s["img"]
    n = s["norms"][0] if s["norms"] else "Saiba mais"
    return (f'<a class="scard" href="{R}{s["slug"]}.html">'
            f'<div class="sc-im"><img src="../assets/img/{f}" alt="{e(alt)}" loading="lazy" width="1200" height="900"><span class="sc-d" aria-hidden="true">{e(s["short"])}</span></div>'
            f'<div class="sc-b"><span class="sc-t">{e(s["title"])}</span><span class="sc-p">{e(s["short"])}</span>'
            f'<span class="sc-n"><span>{e(n)}</span><svg class="arw" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div></a>')''', 1)

# relacionados usam cartoes com imagem
old_rel = '<div class="vis-grid">{\'\'.join(card(x, "") for x in rel[:6])}</div>'
assert old_rel in b
b = b.replace(old_rel, '<div class="scards">{\'\'.join(scard(x, "") for x in rel[:6])}</div>')

# secao 5 nova
i = b.index("# ---------- 5) indice de servicos ----------")
j = b.index("# ---------- 6) politica de privacidade ----------")
NEW5 = r'''# ---------- 5) indice de servicos (filtros + cartoes com imagem) ----------
R = "../"
bc5 = crumbs([("Início", R + "index.html"), ("Serviços", None)])
intro = {
    "projetos": "Elaboração técnica com rigor normativo para segurança, eficiência e integração estrutural em edificações.",
    "vistoria": "Avaliações minuciosas e diagnósticos periciais com embasamento técnico e responsabilidade jurídica.",
    "social": "Projetos de engenharia com valores reduzidos para famílias de baixa renda.",
}
def grp(key, inner):
    return f'<div class="sgrp" data-g="{key}"><div class="head"><h2>{e(CATS[key])}</h2><p>{e(intro[key])}</p></div>{inner}</div>'
def cards(lst):
    return '<div class="scards">' + ''.join(scard(x, "") for x in lst) + '</div>'
PRJ = [x for x in S if x["cat"] == "projetos"]
VIS = [x for x in S if x["cat"] == "vistoria"]
SOC = [x for x in S if x["cat"] == "social"]
parts = [head("Serviços de engenharia civil em Belo Horizonte | CMG Engenharia & Consultoria",
              "Projetos estruturais e complementares, vistorias (cautelar, reforma, entrega, NBR 15575), inspeção predial, perícia estrutural e Engenharia Social em Belo Horizonte, MG.", R), header(R)]
parts.append(f"""<section class="pg-hero compact"><div class="wrap">{bc5}<h1>Nossos Serviços</h1><p class="lead">Soluções completas com responsabilidade técnica e precisão.</p></div></section>
<section class="blk" style="padding-top:var(--s5)"><div class="wrap">
<div class="tabs" role="group" aria-label="Filtrar serviços por categoria"><button type="button" class="tab" data-t="all" aria-pressed="true">Todos</button><button type="button" class="tab" data-t="projetos" aria-pressed="false">Projetos Complementares</button><button type="button" class="tab" data-t="vistoria" aria-pressed="false">Vistoria e Perícia</button><button type="button" class="tab" data-t="social" aria-pressed="false">Engenharia Social</button></div>
<p class="svc-hint" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.8v.1"/></svg>Passe o mouse sobre um serviço para ver uma breve descrição.</p>
""")
parts.append(grp("projetos", cards(PRJ)))
parts.append(grp("vistoria", '<h3 class="sub">Vistoria</h3>' + cards(VIS[:4]) + '<h3 class="sub">Inspeção e perícia</h3>' + cards(VIS[4:])))
parts.append(grp("social", cards(SOC)))
parts.append("</div></section>")
parts.append(cta_band(R, "Olá, gostaria de solicitar um orçamento."))
parts.append("""<script>
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tab')),grps=[].slice.call(document.querySelectorAll('.sgrp'));
  function show(t){
    tabs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===t?'true':'false');});
    grps.forEach(function(g){
      var on=(t==='all'||g.dataset.g===t);
      if(on){g.hidden=false;requestAnimationFrame(function(){g.classList.remove('out');});}
      else{g.hidden=true;g.classList.add('out');}
    });
    if(history.replaceState)history.replaceState(null,'',t==='all'?location.pathname:'#'+t);
  }
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});
  var h=location.hash.slice(1);
  if(['projetos','vistoria','social'].indexOf(h)>-1)show(h);
})();
</script>""")
parts.append(footer(R))
open(os.path.join(ROOT, "servicos", "index.html"), "w", encoding="utf8").write(''.join(parts))

'''
b = b[:i] + NEW5 + b[j:]
open(bp, "w", encoding="utf8").write(b)

# ============ index.html (home) ============
ip = os.path.join(ROOT, "index.html")
s = open(ip, encoding="utf8").read()
s, n = re.subn(r'<nav class="main" id="nav">.*?</nav>', lambda m: '<nav class="main" id="nav">' + nav_html("", home=True) + '</nav>', s, count=1, flags=re.S)
assert n == 1
old1 = "$('#burger').addEventListener('click', function(){ $('#nav').classList.toggle('open'); });\n"
old2 = "$$('#nav a').forEach(function(a){ a.addEventListener('click', function(){ $('#nav').classList.remove('open'); }); });\n"
assert old1 in s and old2 in s
s = s.replace(old1, "").replace(old2, "")
assert "</body>" in s
s = s.replace("</body>", '<script src="assets/js/nav.js"></script>\n</body>', 1)
open(ip, "w", encoding="utf8").write(s)
print("patch2 aplicado")
