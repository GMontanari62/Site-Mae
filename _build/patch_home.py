# -*- coding: utf-8 -*-
"""Atualiza a home (index.html) com as informacoes do site anterior. Rodar uma vez."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = open(P, encoding="utf8").read()

def rep(old, new, count=1):
    global s
    assert old in s, "nao achei: " + old[:70]
    s = s.replace(old, new, count)

# --- logos e nav ---
rep('<img src="assets/img/logo.webp" alt="CMG Projetos &amp; Consultoria">\n    <div class="loader-bar">',
    '<img src="assets/img/logo-completa.webp" alt="CMG Projetos &amp; Consultoria" width="770" height="470">\n    <div class="loader-bar">')
rep('<a class="brand" href="#inicio" aria-label="CMG Engenharia e Consultoria, início"><img src="assets/img/logo.webp" alt="CMG Projetos &amp; Consultoria"></a>',
    '<a class="brand" href="#inicio" aria-label="CMG Engenharia e Consultoria, início"><img src="assets/img/logo-cmg.webp" alt="CMG Engenharia e Consultoria" width="440" height="470"></a>')
rep('<a class="lnk" href="#projetar">Projetos</a>', '<a class="lnk" href="servicos/index.html">Serviços</a>')
rep('<a class="lnk" href="#social">Engenharia Social</a>', '<a class="lnk" href="servicos/engenharia-social.html">Engenharia Social</a>')
rep('<a class="btn btn-ghost" href="#projetar">Conhecer os serviços</a>', '<a class="btn btn-ghost" href="servicos/index.html">Conhecer os serviços</a>')

# --- Projetar: titulos viram links ---
for title, slug in [("Estrutura de concreto e alvenaria", "estrutura-concreto-alvenaria"),
                    ("Instalações hidrossanitárias", "instalacoes-hidrossanitarias"),
                    ("Instalações elétricas de baixa tensão", "instalacoes-eletricas-baixa-tensao")]:
    rep(f'<h3>{title}</h3>', f'<h3><a class="tl-link" href="servicos/{slug}.html">{title}</a></h3>')

# --- Diagnosticar: cartoes viram links das paginas ---
cards = {"Vistoria cautelar": "vistoria-cautelar", "Inspeção predial": "inspecao-predial",
         "Perícia estrutural e patologias": "pericia-estrutural", "Vistoria de reforma": "vistoria-de-reforma",
         "Vistoria de entrega de imóvel": "vistoria-de-entrega-de-imovel", "Atendimento à NBR 15575": "vistoria-nbr-15575"}
def fix_card(m):
    block = m.group(0)
    h = re.search(r"<h3>(.*?)</h3>", block).group(1)
    slug = cards[h]
    block = re.sub(r'<article class="card plain rv" style="(--i:\d)">', rf'<a class="card plain rv" style="\1" href="servicos/{slug}.html">', block)
    return block.replace("</article>", "</a>")
s, n = re.subn(r'<article class="card plain rv".*?</article>', fix_card, s, flags=re.S)
assert n == 6, n

# --- pilares (do site anterior) logo apos a faixa de prova ---
pill = '''<!-- ============ PILARES ============ -->
<section class="pillars-s">
  <div class="wrap pillars">
    <div class="rv" style="--i:0"><span class="n">01</span><h3>Precisão em cada projeto</h3><p>Cada projeto é desenvolvido com base nas mais rigorosas normas técnicas.</p></div>
    <div class="rv" style="--i:1"><span class="n">02</span><h3>Experiência em cada decisão</h3><p>Mais de 35 anos de experiência no mercado, com atendimento personalizado e consultoria especializada.</p></div>
    <div class="rv" style="--i:2"><span class="n">03</span><h3>Confiança em cada etapa</h3><p>Suporte técnico completo durante todo o projeto, com prazos de entrega otimizados.</p></div>
  </div>
</section>

'''
rep('<!-- ============ PROJETAR ============ -->', pill + '<!-- ============ PROJETAR ============ -->')

# --- Engenharia Social: botao para a pagina ---
rep('<div class="rv" style="margin-top:32px"><a class="btn btn-primary" href="#contato">Falar sobre Engenharia Social</a></div>',
    '<div class="rv hero-cta" style="margin-top:32px"><a class="btn btn-primary" href="index.html?servico=Engenharia%20Social#contato">Falar sobre Engenharia Social</a><a class="btn btn-ghost" href="servicos/engenharia-social.html">Saiba mais</a></div>')

# --- formulario: Empresa, opcoes, anexo em linha propria ---
a = s.index('<div class="row">\n        <label>Nome completo *')
b = s.index('<label>Descrição detalhada *')
form = '''<div class="row">
        <label>Nome completo *<input type="text" name="nome" required autocomplete="name"></label>
        <label>Telefone<input type="tel" name="telefone" autocomplete="tel"></label>
      </div>
      <div class="row">
        <label>E-mail *<input type="email" name="email" required autocomplete="email"></label>
        <label>Empresa<input type="text" name="empresa" autocomplete="organization"></label>
      </div>
      <div class="row">
        <label>Tipo de serviço
          <select name="servico">
            <option value="">Selecione</option>
            <option>Projeto estrutural (concreto e alvenaria)</option>
            <option>Instalações hidrossanitárias</option>
            <option>Instalações elétricas de baixa tensão</option>
            <option>Vistoria de reforma</option>
            <option>Vistoria cautelar</option>
            <option>Vistoria de entrega de imóvel</option>
            <option>Vistoria NBR 15575</option>
            <option>Inspeção predial</option>
            <option>Perícia estrutural</option>
            <option>Engenharia Social</option>
            <option>Outro</option>
          </select>
        </label>
        <label>Localização do projeto<input type="text" name="localizacao" placeholder="Bairro e cidade"></label>
      </div>
      <label>Anexar arquivos (planta, projeto, fotos · até 5 MB)<input type="file" name="attachment" id="anexo" multiple accept=".pdf,.jpg,.jpeg,.png,.webp,.dwg,.doc,.docx,.zip"></label>
      '''
s = s[:a] + form + s[b:]
rep('<p class="note">Anexe projetos, fotos ou laudos, se tiver. Seus dados são usados apenas para retornar o seu contato.</p>',
    '<p class="note">Retornamos em até 48 horas. Seus dados são usados apenas para responder ao seu contato, conforme a <a href="politica-de-privacidade.html" style="text-decoration:underline">Política de Privacidade</a>.</p>')

# --- rodape ---
fa = s.index('<footer>'); fb = s.index('</footer>') + len('</footer>')
footer = '''<footer>
  <div class="wrap">
    <div class="foot">
      <div><img src="assets/img/logo-completa.webp" alt="CMG Projetos &amp; Consultoria" width="770" height="470"><p style="margin-top:16px;font-size:var(--t-sm);max-width:36ch">Engenharia civil com responsabilidade técnica, em Belo Horizonte.</p><p style="margin-top:8px;font-size:var(--t-sm)">CREA 60936/D · Ativo</p></div>
      <div><h4>Navegação</h4><ul>
        <li><a href="#inicio">Home</a></li>
        <li><a href="#sobre">Sobre a engenheira</a></li>
        <li><a href="servicos/index.html">Serviços</a></li>
        <li><a href="#contato">Contato</a></li>
        <li><a href="politica-de-privacidade.html">Política de Privacidade</a></li></ul></div>
      <div><h4>Contato</h4><ul>
        <li><a href="https://wa.me/5531988660712" target="_blank" rel="noopener">WhatsApp (31) 98866-0712</a></li>
        <li><a href="mailto:carla@cmgenge.com.br">carla@cmgenge.com.br</a></li>
        <li>Av. Del Rey, 111 - Sala 101 C, Caiçara<br>Belo Horizonte / MG · CEP 30775-240</li>
        <li>Seg a sex, 8h às 18h</li></ul></div>
    </div>
    <div class="legal">
      <span>© 2026 CMG Engenharia &amp; Consultoria. Todos os direitos reservados. · <a href="politica-de-privacidade.html">Política de Privacidade</a></span>
      <span>Site por <a href="https://verticedigitalbr.com" target="_blank" rel="noopener">Vértice Digital</a></span>
    </div>
  </div>
</footer>'''
s = s[:fa] + footer + s[fb:]

# --- dados estruturados (SEO local) ---
ld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"CMG Engenharia & Consultoria","description":"Engenharia civil: projetos estruturais e complementares, vistorias, inspeção predial e perícia.","telephone":"+55-31-98866-0712","email":"carla@cmgenge.com.br","address":{"@type":"PostalAddress","streetAddress":"Avenida Del Rey, 111 - Sala 101 C","addressLocality":"Belo Horizonte","addressRegion":"MG","postalCode":"30775-240","addressCountry":"BR"},"areaServed":"Minas Gerais","openingHours":"Mo-Fr 08:00-18:00"}
</script>
'''
rep('<link rel="stylesheet" href="assets/css/site.css">\n</head>', '<link rel="stylesheet" href="assets/css/site.css">\n' + ld + '</head>')

# --- video 2 sob demanda + loader so espera o hero ---
rep('poster="assets/img/cena2-poster.webp" muted playsinline preload="auto"', 'poster="assets/img/cena2-poster.webp" muted playsinline preload="none"')
rep("var loader = $('#loader'), released = false, pending = 2;", "var loader = $('#loader'), released = false, pending = 1;")
rep("[v1, v2].forEach(function(v){", "[v1].forEach(function(v){")
rep("paint2(0);\nv2.addEventListener('loadedmetadata', function(){ paint2(c2); });",
    """paint2(0);
v2.addEventListener('loadedmetadata', function(){ paint2(c2); });
/* o video da cena 2 (~17 MB) só começa a baixar quando a seção está perto da tela */
new IntersectionObserver(function(es, o){
  if (es[0].isIntersecting){ v2.preload = 'auto'; v2.load(); o.disconnect(); }
},{rootMargin:'900px 0px'}).observe(box2);

/* ?servico=... (vindo das páginas de serviço) já seleciona o tipo de serviço */
(function(){
  var q = new URLSearchParams(location.search).get('servico'), sel = $('#orc select[name=servico]');
  if (!q || !sel) return;
  Array.prototype.forEach.call(sel.options, function(o){ if (o.text === q) sel.value = o.value; });
})();""")

open(P, "w", encoding="utf8").write(s)
print("home atualizada")
