# -*- coding: utf-8 -*-
"""Ajustes de CELULAR na home (revisao de tamanhos). Rodar uma vez: python -I _build/patch3.py
Desktop nao muda: textos curtos usam .m-only e os longos .d-only (alternados por media query)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = open(P, encoding="utf8").read()
assert "c-slides" not in s, "patch3 ja aplicado"

def rep(old, new, count=1):
    global s
    assert old in s, "nao achei: " + old[:80]
    s = s.replace(old, new, count)

def d(full): return f'<span class="d-only">{full}</span>'
def m(short): return f'<span class="m-only">{short}</span>'

# ---------- pilares: titulo e frase curtos no celular ----------
rep('<h3>Precisão em cada projeto</h3><p>Cada projeto é desenvolvido com base nas mais rigorosas normas técnicas.</p>',
    f'<h3>{m("Precisão")}{d("Precisão em cada projeto")}</h3><p>{m("Normas técnicas rigorosas em cada projeto.")}{d("Cada projeto é desenvolvido com base nas mais rigorosas normas técnicas.")}</p>')
rep('<h3>Experiência em cada decisão</h3><p>Mais de 35 anos de experiência no mercado, com atendimento personalizado e consultoria especializada.</p>',
    f'<h3>{m("Experiência")}{d("Experiência em cada decisão")}</h3><p>{m("Mais de 35 anos de mercado e consultoria especializada.")}{d("Mais de 35 anos de experiência no mercado, com atendimento personalizado e consultoria especializada.")}</p>')
rep('<h3>Confiança em cada etapa</h3><p>Suporte técnico completo durante todo o projeto, com prazos de entrega otimizados.</p>',
    f'<h3>{m("Confiança")}{d("Confiança em cada etapa")}</h3><p>{m("Suporte técnico completo e prazos otimizados.")}{d("Suporte técnico completo durante todo o projeto, com prazos de entrega otimizados.")}</p>')

# ---------- projetar: 3 colunas no celular ----------
rep('<a class="tl-link" href="servicos/estrutura-concreto-alvenaria.html">Estrutura de concreto e alvenaria</a></h3><p>Dimensionamento de concreto armado e de alvenaria autoportante, com projeto completo para edificações residenciais, comerciais e institucionais.</p>',
    f'<a class="tl-link" href="servicos/estrutura-concreto-alvenaria.html">{m("Estrutura")}{d("Estrutura de concreto e alvenaria")}</a></h3><p>{m("Concreto armado e alvenaria autoportante.")}{d("Dimensionamento de concreto armado e de alvenaria autoportante, com projeto completo para edificações residenciais, comerciais e institucionais.")}</p>')
rep('<a class="tl-link" href="servicos/instalacoes-hidrossanitarias.html">Instalações hidrossanitárias</a></h3><p>Projetos de água fria, esgoto sanitário e drenagem predial.</p>',
    f'<a class="tl-link" href="servicos/instalacoes-hidrossanitarias.html">{m("Hidráulica")}{d("Instalações hidrossanitárias")}</a></h3><p>{m("Água fria, esgoto e drenagem.")}{d("Projetos de água fria, esgoto sanitário e drenagem predial.")}</p>')
rep('<a class="tl-link" href="servicos/instalacoes-eletricas-baixa-tensao.html">Instalações elétricas de baixa tensão</a></h3><p>Circuitos, quadros de distribuição e segurança elétrica.</p>',
    f'<a class="tl-link" href="servicos/instalacoes-eletricas-baixa-tensao.html">{m("Elétrica")}{d("Instalações elétricas de baixa tensão")}</a></h3><p>{m("Circuitos, quadros e segurança.")}{d("Circuitos, quadros de distribuição e segurança elétrica.")}</p>')
rep('<div class="rv" style="--i:3;padding-top:24px"><a class="btn btn-primary" href="#contato">Pedir orçamento de projeto</a></div>',
    '<div class="rv proj-cta" style="--i:3;padding-top:24px"><a class="btn btn-primary" href="#contato">Pedir orçamento de projeto</a></div>')

# ---------- processo: linha do tempo (so CSS), classe para o titulo ----------
rep('<section class="blk dark grid-dark">', '<section class="blk dark grid-dark proc">')

# ---------- para quem + normas: uma secao so no celular ----------
rep('<section class="blk">\n  <div class="wrap two">', '<section class="blk qn">\n  <div class="wrap two">\n    <div class="head m-blk"><span class="eyebrow">Quem atendemos</span><h2>Para quem trabalhamos e as normas que seguimos</h2></div>')
for who, txt in [("Proprietários", "Reforma, regularização, entrega de imóvel e dúvidas sobre fissuras."),
                 ("Construtoras", "Vistoria cautelar de vizinhança, projetos e laudos técnicos."),
                 ("Condomínios", "Inspeção predial e diagnóstico de patologias nas áreas comuns.")]:
    rep(f'<strong>{who}</strong>{txt}', f'<strong>{who}</strong><span class="dsc">{txt}</span>')
rep('<div class="head rv" style="margin-bottom:32px"><span class="eyebrow">Para quem trabalhamos</span><h2>Quem precisa de projeto, laudo ou vistoria</h2></div>',
    '<div class="head rv qn-h" style="margin-bottom:32px"><span class="eyebrow">Para quem trabalhamos</span><h2>Quem precisa de projeto, laudo ou vistoria</h2></div>')
rep('<div class="head rv" style="margin-bottom:32px"><span class="eyebrow">Normas que seguimos</span><h2>Rigor técnico em cada documento</h2></div>',
    '<div class="head rv qn-h" style="margin-bottom:32px"><span class="eyebrow">Normas que seguimos</span><h2>Rigor técnico em cada documento</h2></div>')
rep('<b>NBR 15575</b><span>Desempenho de edificações habitacionais.</span>', f'<b>NBR 15575</b><span>{m("Desempenho habitacional")}{d("Desempenho de edificações habitacionais.")}</span>')
rep('<b>NBR 16280</b><span>Reforma em edificações: avaliação técnica prévia.</span>', f'<b>NBR 16280</b><span>{m("Reforma em edificações")}{d("Reforma em edificações: avaliação técnica prévia.")}</span>')
rep('<b>NBR 16747</b><span>Inspeção predial: diretrizes, conceitos e procedimentos.</span>', f'<b>NBR 16747</b><span>{m("Inspeção predial")}{d("Inspeção predial: diretrizes, conceitos e procedimentos.")}</span>')

# ---------- engenharia social: resumo no celular ----------
rep('<p class="rv">Acreditamos que a engenharia deve ser acessível a todos. Por isso, oferecemos projetos de engenharia com valores reduzidos para famílias de baixa renda, contribuindo para que mais pessoas possam construir, reformar ou regularizar seus imóveis com segurança, qualidade e responsabilidade técnica.</p>',
    '<p class="rv">' + m("Projetos de engenharia com valores reduzidos para famílias de baixa renda construírem, reformarem ou regularizarem seus imóveis com segurança e responsabilidade técnica.") + d("Acreditamos que a engenharia deve ser acessível a todos. Por isso, oferecemos projetos de engenharia com valores reduzidos para famílias de baixa renda, contribuindo para que mais pessoas possam construir, reformar ou regularizar seus imóveis com segurança, qualidade e responsabilidade técnica.") + '</p>')
rep('<p class="rv">Nosso objetivo é promover', '<p class="rv d-blk">Nosso objetivo é promover')
rep('<p class="rv">Se você busca uma solução', '<p class="rv d-blk">Se você busca uma solução')
rep('<div class="rv hero-cta" style="margin-top:32px"><a class="btn btn-primary" href="index.html?servico=Engenharia%20Social#contato">Falar sobre Engenharia Social</a><a class="btn btn-ghost" href="servicos/engenharia-social.html">Saiba mais</a></div>',
    '<div class="rv hero-cta soc-cta" style="margin-top:32px"><a class="btn btn-primary" href="servicos/engenharia-social.html">Saiba mais</a><a class="btn btn-ghost" href="index.html?servico=Engenharia%20Social#contato">Falar com a CMG</a></div>')

# ---------- contato: cabecalho + paineis (abas) + mapa ----------
a = s.index('<div class="wrap contact">')
fa = s.index('<form class="rv" id="orc"')
fb = s.index('</form>', fa) + len('</form>')
form = s[fa:fb].replace('<form class="rv" id="orc"', '<form class="rv c-form" id="orc"', 1)
tail_end = s.index('</section>', fb)
wa = 'https://wa.me/5531988660712?text=Ol%C3%A1%2C%20gostaria%20de%20solicitar%20um%20or%C3%A7amento.'
contact = f'''<div class="wrap contact">
    <div class="head rv c-head" style="margin-bottom:0"><span class="eyebrow">Contato</span><h2>Vamos conversar sobre o seu projeto ou vistoria</h2><p>Estamos à disposição para atender você.</p></div>
    <div class="c-tabs" role="tablist" aria-label="Escolha entre informações e formulário"><button type="button" role="tab" aria-selected="true" data-i="0">Informações</button><button type="button" role="tab" aria-selected="false" data-i="1">Formulário</button></div>
    <div class="c-slides" id="cslides">
      <div class="c-info">
        <div class="info rv">
          <div><small>Telefone</small><a href="tel:+5531988660712">+55 (31) 98866-0712</a></div>
          <div><small>WhatsApp</small><a href="{wa}" target="_blank" rel="noopener">+55 (31) 98866-0712</a></div>
          <div><small>E-mail</small><a href="mailto:carla@cmgenge.com.br">carla@cmgenge.com.br</a></div>
          <div><small>Localização</small>Avenida Del Rey, 111 - Sala 101 C<br>Bairro Caiçara, Belo Horizonte / MG</div>
          <div><small>Horário de atendimento</small>Segunda a sexta, das 8h às 18h</div>
        </div>
        <div class="rv hero-cta" style="margin-top:32px"><a class="btn btn-primary" href="tel:+5531988660712">Ligar agora</a><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">Chamar no WhatsApp</a></div>
      </div>
      {form}
    </div>
    <div class="map rv c-map"><iframe title="Mapa: Avenida Del Rey, 111, Caiçara, Belo Horizonte" loading="lazy" src="https://www.google.com/maps?q=Avenida+Del+Rey+111+Cai%C3%A7ara+Belo+Horizonte&output=embed"></iframe></div>
  </div>
'''
s = s[:a] + contact + s[tail_end:]

# ---------- script: hero (texto aparece com o scroll), abas do contato ----------
rep("hint.style.opacity = p > 0.03 ? 0 : 1;",
    """hint.style.opacity = p > 0.03 ? 0 : 1;
  /* celular: título e botão nascem de 30% a 70% da animação; no desktop não mexe */
  if (isMobile()){
    var o = clamp((p - 0.3) / 0.4, 0, 1);
    heroCopy.style.opacity = o;
    heroCopy.style.transform = 'translateY(' + ((1 - o) * 14) + 'px)';
    heroCopy.style.pointerEvents = o < 0.4 ? 'none' : 'auto';
  } else {
    heroCopy.style.opacity = ''; heroCopy.style.transform = ''; heroCopy.style.pointerEvents = '';
  }""")
rep("var heroSec = $('#inicio'), v1 = $('#v1');", "var heroSec = $('#inicio'), v1 = $('#v1'), heroCopy = $('.hero-copy');")
rep("/* ===== anexos: limite de 5 MB no total ===== */",
    """/* ===== contato no celular: painéis Informações | Formulário ===== */
(function(){
  var slides = $('#cslides'), tabs = $$('.c-tabs button');
  if (!slides || !tabs.length) return;
  var mq = window.matchMedia('(max-width:768px)');
  function cur(){ return Math.round(slides.scrollLeft / Math.max(1, slides.clientWidth)); }
  function sync(){
    if (!mq.matches){ slides.style.height = ''; return; }
    var i = cur(), panel = slides.children[i];
    tabs.forEach(function(b, k){ b.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    if (panel) slides.style.height = panel.offsetHeight + 'px';
  }
  function go(i){ slides.scrollTo({left: i * slides.clientWidth, behavior: 'smooth'}); }
  tabs.forEach(function(b){ b.addEventListener('click', function(){ go(+b.dataset.i); }); });
  var t = null;
  slides.addEventListener('scroll', function(){ clearTimeout(t); t = setTimeout(sync, 80); }, {passive:true});
  window.addEventListener('resize', sync);
  if (/servico=/.test(location.search) && mq.matches) slides.scrollLeft = slides.clientWidth;
  sync();
  setTimeout(sync, 600);
})();

/* ===== anexos: limite de 5 MB no total ===== */""")

open(P, "w", encoding="utf8").write(s)
print("patch3 aplicado")
