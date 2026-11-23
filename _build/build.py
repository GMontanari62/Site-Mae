# -*- coding: utf-8 -*-
"""Gera as paginas internas do site CMG (servicos, privacidade).
Uso: python _build/build.py   (rodar a partir da pasta cmg-engenharia)
Esta pasta _build NAO vai para a hospedagem."""
import os, re, sys, html, urllib.parse, time
VER = time.strftime('%Y%m%d%H%M')   # carimbo de versao nos links de CSS/JS (cache de 1 mes na hospedagem)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import nav_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = "5531988660712"

# Paginas de servico que ja usam o novo layout de celular (classe body.ref).
# Para estender a todas: REF = set(todos os slugs).
REF = {"vistoria-cautelar"}
REF_SCRIPT = """<script>
/* painéis "Por que escolher | Informações" (celular): abas + deslize, altura acompanha o painel ativo */
(function(){
  var s=document.getElementById('pnSlides'),tabs=[].slice.call(document.querySelectorAll('.pn-tabs button')),mq=window.matchMedia('(max-width:768px)'),t=null;
  if(!s||!tabs.length)return;
  function cur(){return Math.round(s.scrollLeft/Math.max(1,s.clientWidth));}
  /* marca a aba e ajusta a altura NA HORA (sem esperar o fim da rolagem) */
  function setActive(i){
    if(!mq.matches){s.style.height='';return;}
    var p=s.children[i];
    tabs.forEach(function(b,k){b.setAttribute('aria-selected',k===i?'true':'false');});
    if(p)s.style.height=p.offsetHeight+'px';
  }
  function sync(){setActive(cur());}
  var lock=null,lockT=null,raf=null;
  function go(i){
    lock=i;clearTimeout(lockT);lockT=setTimeout(function(){lock=null;},800);
    setActive(i);
    s.scrollTo({left:i*s.clientWidth,behavior:'smooth'});
  }
  tabs.forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.i);});});
  var ft=null;
  function onScroll(){
    var i=cur();
    if(lock!==null){if(i===lock)lock=null;else return;}
    if(tabs[i]&&tabs[i].getAttribute('aria-selected')!=='true')setActive(i);
  }
  s.addEventListener('scroll',function(){
    if(!raf)raf=requestAnimationFrame(function(){raf=null;onScroll();});
    clearTimeout(ft);ft=setTimeout(onScroll,70);
  },{passive:true});
  window.addEventListener('resize',sync);sync();setTimeout(sync,600);
})();
/* pontinhos do carrossel "Veja também" (só aparecem no celular) */
(function(){
  var c=document.querySelector('.rel .scards');if(!c||c.children.length<2)return;
  var n=c.children.length,d=document.createElement('div');d.className='dots';
  for(var i=0;i<n;i++)d.appendChild(document.createElement('i'));
  c.parentNode.insertBefore(d,c.nextSibling);
  function upd(){var w=c.children[0].offsetWidth+12;var k=(c.scrollLeft+c.clientWidth>=c.scrollWidth-4)?n-1:Math.round(c.scrollLeft/Math.max(1,w));[].forEach.call(d.children,function(x,j){x.classList.toggle('on',j===k);});}
  c.addEventListener('scroll',function(){requestAnimationFrame(upd);},{passive:true});
  window.addEventListener('resize',upd);upd();
})();
</script>"""

# ---------- 1) CSS: tira o <style> do index e cria assets/css/site.css (uma vez) ----------
idx_path = os.path.join(ROOT, "index.html")
idx = open(idx_path, encoding="utf8").read()
m = re.search(r"<style>(.*?)</style>", idx, flags=re.S)
os.makedirs(os.path.join(ROOT, "assets", "css"), exist_ok=True)
if m:
    open(os.path.join(ROOT, "assets", "css", "site.css"), "w", encoding="utf8").write(m.group(1).strip() + "\n")
    idx = idx.replace(m.group(0), '<link rel="stylesheet" href="assets/css/site.css">')
    open(idx_path, "w", encoding="utf8").write(idx)
    print("CSS extraido para assets/css/site.css")

# ---------- 2) dados dos servicos (textos do site anterior da Carla) ----------
WHY = [
    "Mais de 35 anos de experiência no mercado",
    "Conformidade com todas as normas técnicas vigentes",
    "Atendimento personalizado e consultoria especializada",
    "Prazos de entrega otimizados",
    "Suporte técnico completo durante todo o projeto",
]
CATS = {
    "projetos": "Projetos Complementares",
    "vistoria": "Vistoria e Perícia",
    "social": "Engenharia Social",
}
S = [
    dict(slug="estrutura-concreto-alvenaria", cat="projetos", title="Estrutura de Concreto e Alvenaria",
         short="Dimensionamento de concreto armado e alvenaria autoportante.",
         norms=["NBR 6118", "NBR 6120", "NBR 16868"], img=("projeto.webp", "Prancheta de engenharia com projeto estrutural, régua e capacete"),
         p=["A elaboração de projetos estruturais é fundamental para a segurança e a durabilidade de qualquer edificação. Cada projeto é desenvolvido com base nas mais rigorosas normas técnicas, garantindo estabilidade estrutural e a otimização dos recursos investidos na obra.",
            "A atuação abrange estruturas em concreto armado e alvenaria autoportante, com soluções personalizadas para diferentes tipos de construção, desde residências unifamiliares até edifícios comerciais de grande porte. Cada empreendimento recebe análise e dimensionamento próprios, respeitando suas características e necessidades específicas.",
            "O objetivo é integrar a estrutura à arquitetura, unindo funcionalidade e estética, para que o projeto estrutural sustente a visão do projeto como um todo, sem comprometer a segurança nem a viabilidade técnica e econômica."]),
    dict(slug="instalacoes-hidrossanitarias", cat="projetos", title="Instalações Hidrossanitárias",
         short="Projetos de água fria, esgoto sanitário e drenagem predial.",
         norms=["NBR 8160", "NBR 5626", "NBR 7229"], img=None,
         p=["Projetamos sistemas hidrossanitários eficientes e seguros, garantindo o correto abastecimento de água e o descarte adequado de efluentes. Nossos projetos visam a economia de água, a durabilidade dos sistemas e a conformidade com as normas de saúde e saneamento.",
            "Incluímos dimensionamento de tubulações, reservatórios, sistemas de aquecimento de água, e soluções para reuso de água, sempre buscando a sustentabilidade e a funcionalidade para o usuário."]),
    dict(slug="instalacoes-eletricas-baixa-tensao", cat="projetos", title="Instalações Elétricas de Baixa Tensão",
         short="Circuitos, quadros de distribuição e segurança elétrica.",
         norms=["NBR 5410", "NBR 14039", "NR 10"], img=None,
         p=["Desenvolvemos projetos elétricos prediais que garantem a segurança dos usuários, a eficiência energética e a funcionalidade dos sistemas. Dimensionamos circuitos, quadros de distribuição, sistemas de aterramento e proteção contra surtos.",
            "Nossos projetos consideram as necessidades específicas de cada edificação, desde residências até complexos comerciais, sempre em conformidade com as normas de segurança e as melhores práticas do setor."]),
    dict(slug="vistoria-de-reforma", cat="vistoria", title="Vistoria de Reforma",
         short="Avaliação técnica para reformas conforme a NBR 16280.",
         norms=["NBR 16280", "ABNT NBR 14037"], img=None,
         p=["A vistoria de reforma é essencial para garantir que as modificações em edificações existentes sejam realizadas de forma segura e em conformidade com as normas técnicas. Avaliamos o impacto da reforma na estrutura, instalações e segurança do imóvel, emitindo um laudo técnico com as diretrizes e recomendações necessárias.",
            "Nosso serviço abrange desde pequenas reformas residenciais até grandes intervenções em edifícios comerciais, protegendo o proprietário e garantindo a integridade da edificação e de seus vizinhos."]),
    dict(slug="vistoria-cautelar", cat="vistoria", title="Vistoria Cautelar",
         short="Documentação de imóveis vizinhos para proteção legal.",
         norms=["NBR 13752", "Código Civil Brasileiro", "Código de Processo Civil", "Resolução CONFEA 345/90"],
         img=("cautelar.webp", "Casa vizinha a uma obra em construção, com linha técnica de medição"),
         p=["A Vistoria Cautelar é um documento técnico que registra as condições físicas de um imóvel em determinado momento, servindo como prova em processos judiciais, seguros ou para proteção patrimonial. Este serviço é fundamental para documentar o estado de conservação de imóveis antes de obras vizinhas, locações, compra e venda, ou qualquer situação que possa gerar questionamentos futuros sobre danos.",
            "O laudo cautelar detalha fissuras, trincas, rachaduras, condições de pintura e revestimentos, funcionamento de instalações e inclui registro fotográfico detalhado, protegendo o proprietário contra futuras reclamações."]),
    dict(slug="vistoria-de-entrega-de-imovel", cat="vistoria", title="Vistoria de Entrega de Imóvel",
         short="Verificação técnica na entrega de chaves de imóveis.",
         norms=["NBR 15575", "Código de Defesa do Consumidor", "Lei 4.591/64", "NBR 5674"], img=None,
         p=["A Vistoria de Entrega de Imóvel é uma avaliação técnica realizada no momento da entrega de imóveis novos ou reformados, verificando se a obra foi executada conforme o projeto e as especificações técnicas. Este serviço protege o comprador ou locatário, identificando defeitos, não conformidades e itens que necessitam de correção antes da entrega definitiva do imóvel.",
            "Verificamos acabamentos, revestimentos, funcionamento de instalações, esquadrias, vedações, sistemas elétricos e hidráulicos, e a conformidade com o memorial descritivo, garantindo que o imóvel seja entregue em perfeitas condições."]),
    dict(slug="vistoria-nbr-15575", cat="vistoria", title="Vistoria de Atendimento à NBR 15575",
         short="Avaliação de desempenho de edificações habitacionais.",
         norms=["NBR 15575", "NBR 15220", "NBR 15292", "Instruções Técnicas do Corpo de Bombeiros"], img=None,
         p=["A Vistoria de atendimento à NBR 15575 avalia o desempenho de edificações habitacionais, verificando se atendem aos requisitos mínimos de desempenho estrutural, segurança contra incêndio, estanqueidade, conforto térmico, acústico e durabilidade. Esta norma estabelece critérios e métodos para avaliação do desempenho de edificações habitacionais, sendo obrigatória para empreendimentos financiados pelo Sistema Financeiro da Habitação.",
            "Avaliamos sistemas estruturais, pisos, vedações, coberturas e instalações, e verificamos o desempenho estrutural, segurança contra incêndio, segurança no uso e operação, estanqueidade à água, desempenho térmico, desempenho acústico, durabilidade e manutenibilidade."]),
    dict(slug="inspecao-predial", cat="vistoria", title="Inspeção Predial",
         short="Avaliação técnica das condições de uso, operação e manutenção.",
         norms=["NBR 16747", "IBAPE"], img=("inspecao.webp", "Técnico com capacete inspecionando a fachada de um edifício"),
         p=["A inspeção predial é um diagnóstico técnico que avalia o estado geral de conservação de uma edificação, identificando anomalias, falhas e vícios construtivos. Nosso trabalho visa prevenir problemas maiores, otimizar a manutenção e garantir a segurança e a valorização do imóvel.",
            "Realizamos vistorias detalhadas em todas as áreas da edificação, incluindo estrutura, instalações, acabamentos e sistemas de segurança, emitindo um laudo técnico com recomendações para as devidas correções e manutenções."]),
    dict(slug="pericia-estrutural", cat="vistoria", title="Perícia Estrutural e Análise de Patologias",
         short="Investigação de fissuras, patologias e laudos periciais conclusivos.",
         norms=["NBR 13752", "NBR 6118", "NBR 8800", "NBR 7190", "Resolução CONFEA 345/90"], img=None,
         p=["A Perícia Estrutural é uma investigação técnica especializada que visa identificar as causas de problemas estruturais, patologias construtivas e determinar as medidas corretivas necessárias para garantir a segurança da edificação. Este serviço é fundamental em casos de sinistros, processos judiciais, ou quando há suspeita de problemas estruturais que possam comprometer a segurança dos usuários.",
            "Investigamos fissuras, trincas, rachaduras, problemas de fundação, corrosão de armaduras, infiltrações, umidade, deformações excessivas, falhas de execução e problemas de projeto, utilizando inspeção visual detalhada, ensaios não destrutivos, análise de projetos e documentos, e modelagem estrutural para emitir um relatório técnico conclusivo."]),
    dict(slug="engenharia-social", cat="social", title="Engenharia Social",
         short="Projetos de engenharia com valores reduzidos para famílias de baixa renda.",
         norms=[], img=("social.webp", "Família diante de sua casa em reforma, com uma planta de engenharia em primeiro plano"),
         p=["Acreditamos que a engenharia deve ser acessível a todos. Por isso, oferecemos projetos de engenharia com valores reduzidos para famílias de baixa renda, contribuindo para que mais pessoas possam construir, reformar ou regularizar seus imóveis com segurança, qualidade e responsabilidade técnica.",
            "Nosso objetivo é promover inclusão social por meio da engenharia, garantindo acesso a serviços profissionais essenciais, como projetos arquitetônicos, estruturais, elétricos, hidráulicos e documentações técnicas, sempre respeitando as normas vigentes e as necessidades de cada família.",
            "Se você busca uma solução técnica confiável e com custo acessível, entre em contato conosco. Juntos, podemos transformar sonhos em realidade, tornando a construção civil mais justa, segura e acessível para todos."],
         quote="Engenharia com responsabilidade social, construindo oportunidades e melhorando vidas."),
]
BY_SLUG = {s["slug"]: s for s in S}
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
    BY_SLUG[_k]["img"] = _v

# Layout de celular das paginas individuais: aprovado, vale para todas.
# (Para voltar a uma pagina so: REF = {"vistoria-cautelar"})
REF = set(BY_SLUG)
FORM_NAME = {  # texto da opcao no formulario da home
    "estrutura-concreto-alvenaria": "Projeto estrutural (concreto e alvenaria)",
    "instalacoes-hidrossanitarias": "Instalações hidrossanitárias",
    "instalacoes-eletricas-baixa-tensao": "Instalações elétricas de baixa tensão",
    "vistoria-de-reforma": "Vistoria de reforma",
    "vistoria-cautelar": "Vistoria cautelar",
    "vistoria-de-entrega-de-imovel": "Vistoria de entrega de imóvel",
    "vistoria-nbr-15575": "Vistoria NBR 15575",
    "inspecao-predial": "Inspeção predial",
    "pericia-estrutural": "Perícia estrutural",
    "engenharia-social": "Engenharia Social",
}

e = html.escape

def scard(s, R):
    f, alt = s["img"]
    n = s["norms"][0] if s["norms"] else "Saiba mais"
    return (f'<a class="scard" href="{R}{s["slug"]}.html">'
            f'<div class="sc-im"><img src="../assets/img/{f}" alt="{e(alt)}" loading="lazy" width="1200" height="900"><span class="sc-d" aria-hidden="true">{e(s["short"])}</span></div>'
            f'<div class="sc-b"><span class="sc-t">{e(s["title"])}</span><span class="sc-p">{e(s["short"])}</span>'
            f'<span class="sc-n"><span>{e(n)}</span><svg class="arw" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div></a>')

# ---------- 3) pedacos comuns ----------
def head(title, desc, R):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0e1c2e">
<meta name="color-scheme" content="only light">
<link rel="icon" href="{R}assets/img/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/pages.min.css?v={VER}">
</head>
<body class="sub">
'''

def header(R):
    return f'''<header class="top solid" id="top">
  <div class="wrap">
    <a class="brand" href="{R}index.html" aria-label="CMG Engenharia e Consultoria, início"><img src="{R}assets/img/logo-cmg.webp" alt="CMG Engenharia e Consultoria" width="440" height="470"></a>
    <button class="burger" id="burger" aria-label="Abrir menu"><span></span><span></span></button>
    <nav class="main" id="nav">{nav_html(R)}</nav>
  </div>
</header>
'''

def footer(R):
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div><img src="{R}assets/img/logo-completa.webp" alt="CMG Projetos &amp; Consultoria" width="770" height="470"><p style="margin-top:16px;font-size:var(--t-sm);max-width:36ch">Engenharia civil com responsabilidade técnica, em Belo Horizonte.</p><p style="margin-top:8px;font-size:var(--t-sm)">CREA 60936/D · Ativo</p></div>
      <div><h3>Navegação</h3><ul>
        <li><a href="{R}index.html">Home</a></li>
        <li><a href="{R}index.html#sobre">Sobre a engenheira</a></li>
        <li><a href="{R}servicos/index.html">Serviços</a></li>
        <li><a href="{R}blog/index.html">Blog</a></li>
        <li><a href="{R}index.html#contato">Contato</a></li>
        <li><a href="{R}politica-de-privacidade.html">Política de Privacidade</a></li></ul></div>
      <div><h3>Contato</h3><ul>
        <li><a href="tel:+{WA}">Telefone (31) 98866-0712</a></li>
        <li><a href="https://wa.me/{WA}?text=Ol%C3%A1%2C%20gostaria%20de%20solicitar%20um%20or%C3%A7amento." target="_blank" rel="noopener">WhatsApp (31) 98866-0712</a></li>
        <li><a href="mailto:carla@cmgenge.com.br">carla@cmgenge.com.br</a></li>
        <li>Av. Del Rey, 111 - Sala 101 C, Caiçara<br>Belo Horizonte / MG · CEP 30775-240</li>
        <li>Seg a sex, 8h às 18h</li></ul></div>
    </div>
    <div class="legal">
      <span>© 2026 CMG Engenharia &amp; Consultoria. Todos os direitos reservados. · <a href="{R}politica-de-privacidade.html">Política de Privacidade</a> · <a href="{R}admin/" rel="nofollow">Área da editora</a></span>
      <span>Site por <a href="https://verticedigitalbr.com" target="_blank" rel="noopener">Vértice Digital</a></span>
    </div>
  </div>
</footer>
<script src="{R}assets/js/nav.js?v={VER}"></script>
</body>
</html>
'''

def crumbs(items):
    out = []
    for i, (label, href) in enumerate(items):
        out.append(f'<a href="{href}">{e(label)}</a>' if href else f'<b>{e(label)}</b>')
    return '<nav class="crumbs" aria-label="Caminho">' + ' <span>/</span> '.join(out) + '</nav>'

def cta_band(R, text):
    return f'''<section class="band"><div class="wrap band-in">
  <div><h2>Solicite um orçamento</h2><p>Estamos à disposição para atender seu projeto ou vistoria técnica.</p></div>
  <div class="cta-row"><a class="btn btn-primary" href="{R}index.html#contato">Solicitar orçamento</a><a class="btn btn-wa" href="https://wa.me/{WA}?text={urllib.parse.quote(text)}" target="_blank" rel="noopener">Chamar no WhatsApp</a></div>
</div></section>
'''

def card(s, R):
    pills = ''.join(f'<span class="norma">{e(n)}</span> ' for n in s["norms"][:1])
    return f'''<a class="card plain" href="{R}{s["slug"]}.html"><div class="ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div><div class="bd"><h3>{e(s["title"])}</h3><p>{e(s["short"])}</p>{pills}</div></a>'''

# ---------- 4) paginas de servico ----------
os.makedirs(os.path.join(ROOT, "servicos"), exist_ok=True)
for s in S:
    R = "../"
    cat = CATS[s["cat"]]
    desc = s["p"][0]
    desc = (desc[:152].rsplit(" ", 1)[0] + "…") if len(desc) > 155 else desc
    title = f'{s["title"]} em BH | CMG Engenharia'
    parts = [head(title, desc, R), header(R)]
    bc = crumbs([("Início", R + "index.html"), ("Serviços", "index.html"), (s["title"], None)] if s["cat"] == "social"
                else [("Início", R + "index.html"), ("Serviços", "index.html"), (cat, "index.html#" + s["cat"]), (s["title"], None)])
    pills = ''.join(f'<span class="npill">{e(n)}</span>' for n in s["norms"])
    pills = f'<div class="npills" aria-label="Normas deste serviço">{pills}</div>' if pills else ''
    parts.append(f'''<section class="pg-hero"><div class="wrap">{bc}<span class="eyebrow">{e(cat)}</span><h1>{e(s["title"])}</h1>{pills}</div></section>
''')
    img = ''
    if s["img"]:
        img = f'<figure class="svc-img"><img src="{R}assets/img/{s["img"][0]}" alt="{e(s["img"][1])}" loading="lazy" width="1200" height="900"><span class="tag-ill">Imagem ilustrativa</span></figure>'
    paras = ''.join(f'<p>{e(p)}</p>' for p in s["p"])
    quote = f'<blockquote class="sq">{e(s["quote"])}</blockquote>' if s.get("quote") else ''
    why = ''.join(f'<li>{e(w)}</li>' for w in WHY)
    form_opt = urllib.parse.quote(FORM_NAME[s["slug"]])
    wa_text = f'Olá, gostaria de solicitar um orçamento de {s["title"]}.'
    cta_html = (f'<div class="cta-row"><a class="btn btn-primary" href="{R}index.html?servico={form_opt}#contato">Solicitar orçamento</a>'
                f'<a class="btn btn-wa" href="https://wa.me/{WA}?text={urllib.parse.quote(wa_text)}" target="_blank" rel="noopener">Chamar no WhatsApp</a></div>')
    info_dl = ('<dt>CREA</dt><dd>60936/D · Registro ativo</dd><dt>Especialização</dt><dd>Mestre em Engenharia de Estruturas</dd>'
               '<dt>Área de atuação</dt><dd>Minas Gerais</dd><dt>Tempo de resposta</dt><dd>24 a 48 horas</dd>')
    if s["slug"] in REF:
        # celular: "Por que escolher" e "Informações" viram 2 paineis com abas (no desktop o painel de informacoes fica oculto)
        why_block = (f'<div class="pn" id="pn"><div class="pn-tabs" role="tablist" aria-label="Escolha o conteúdo">'
                     f'<button type="button" role="tab" aria-selected="true" data-i="0">Por que escolher</button>'
                     f'<button type="button" role="tab" aria-selected="false" data-i="1">Informações</button></div>'
                     f'<div class="pn-slides" id="pnSlides"><div class="pn-why"><h2>Por que escolher nossos serviços?</h2><ul class="why">{why}</ul></div>'
                     f'<div class="info-card pn-info"><h2>Informações adicionais</h2><dl>{info_dl}</dl></div></div>{cta_html}</div>')
    else:
        why_block = f'<h2>Por que escolher nossos serviços?</h2>\n<ul class="why">{why}</ul>\n{cta_html}'
    parts.append(f'''<section class="blk"><div class="wrap svc-layout">
<article>
{img}
<h2>Detalhes do serviço</h2>
{paras}
{quote}
{why_block}
</article>
<aside class="info-card"><h2>Informações adicionais</h2><dl>
<dt>CREA</dt><dd>60936/D · Registro ativo</dd>
<dt>Especialização</dt><dd>Mestre em Engenharia de Estruturas</dd>
<dt>Área de atuação</dt><dd>Minas Gerais</dd>
<dt>Tempo de resposta</dt><dd>24 a 48 horas</dd>
</dl><a class="btn btn-primary" href="{R}index.html?servico={form_opt}#contato">Solicitar orçamento</a></aside>
</div></section>
''')
    rel = [x for x in S if x["cat"] == s["cat"] and x["slug"] != s["slug"]]
    if not rel:
        rel = [x for x in S if x["slug"] != s["slug"]][:3]
    parts.append(f'''<section class="blk rel"><div class="wrap"><div class="head"><span class="eyebrow">Veja também</span><h2>Outros serviços</h2></div><div class="scards">{''.join(scard(x, "") for x in rel[:6])}</div><p style="margin-top:24px"><a class="back" href="index.html">← Ver todos os serviços</a></p></div></section>
''')
    if s["slug"] in REF:
        parts.append(REF_SCRIPT)
    parts.append(cta_band(R, wa_text))
    parts.append(footer(R))
    page_html = ''.join(parts)
    if s["slug"] in REF:   # pagina de referencia do layout de celular (as outras entram depois)
        page_html = page_html.replace('<body class="sub">', '<body class="sub ref">', 1)
    open(os.path.join(ROOT, "servicos", s["slug"] + ".html"), "w", encoding="utf8").write(page_html)

# ---------- 5) indice de servicos (filtros + cartoes com imagem) ----------
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
    return '<div class="scards' + (' one' if len(lst) == 1 else '') + '">' + ''.join(scard(x, "") for x in lst) + '</div>'
PRJ = [x for x in S if x["cat"] == "projetos"]
VIS = [x for x in S if x["cat"] == "vistoria"]
SOC = [x for x in S if x["cat"] == "social"]
parts = [head("Serviços de Engenharia Civil em BH | CMG Engenharia & Consultoria",
              "Projetos, vistorias (cautelar, reforma, entrega, NBR 15575), inspeção predial, perícia estrutural e Engenharia Social em Belo Horizonte, MG.", R), header(R)]
parts.append(f"""<section class="pg-hero compact"><div class="wrap">{bc5}<h1>Nossos Serviços</h1><p class="lead">Soluções completas com responsabilidade técnica e precisão.</p></div></section>
<section class="blk" style="padding-top:var(--s5)"><div class="wrap">
<div class="tabs" role="group" aria-label="Filtrar serviços por categoria"><button type="button" class="tab" data-t="all" aria-pressed="true">Todos</button><button type="button" class="tab" data-t="projetos" aria-pressed="false">Projetos Complementares</button><button type="button" class="tab" data-t="vistoria" aria-pressed="false">Vistoria e Perícia</button><button type="button" class="tab" data-t="social" aria-pressed="false">Engenharia Social</button></div>
<div class="flt" id="flt"><button type="button" class="flt-btn" id="fltBtn" aria-expanded="false" aria-controls="fltPanel"><svg class="flt-i" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h9M19 7h1M4 17h1M11 17h9"/><circle cx="16" cy="7" r="2.2"/><circle cx="8" cy="17" r="2.2"/></svg><span class="flt-l">Filtrar</span><span class="flt-v" id="fltV">Todos</span><svg class="flt-c" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button><div class="flt-p" id="fltPanel" role="listbox" aria-label="Filtrar serviços"><div class="flt-in"><button type="button" class="flt-o" role="option" data-t="all" aria-selected="true"><span>Todos</span><small>10</small></button><button type="button" class="flt-o" role="option" data-t="projetos" aria-selected="false"><span>Projetos Complementares</span><small>3</small></button><button type="button" class="flt-o" role="option" data-t="vistoria" aria-selected="false"><span>Vistoria e Perícia</span><small>6</small></button><button type="button" class="flt-o" role="option" data-t="social" aria-selected="false"><span>Engenharia Social</span><small>1</small></button></div></div></div>
<p class="svc-hint" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.8v.1"/></svg>Passe o mouse sobre um serviço para ver uma breve descrição.</p>
""")
parts.append(grp("projetos", cards(PRJ)))
parts.append(grp("vistoria", '<h3 class="sub">Vistoria</h3>' + cards(VIS[:4]) + '<h3 class="sub">Inspeção e perícia</h3>' + cards(VIS[4:])))
parts.append(grp("social", cards(SOC)))
parts.append("</div></section>")
parts.append(cta_band(R, "Olá, gostaria de solicitar um orçamento."))
parts.append("""<script>
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
</script>""")
parts.append(footer(R))
open(os.path.join(ROOT, "servicos", "index.html"), "w", encoding="utf8").write(''.join(parts))

# ---------- 6) politica de privacidade ----------
R = ""
def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
priv = f'''<section class="pg-hero"><div class="wrap">{crumbs([("Início", "index.html"), ("Política de Privacidade", None)])}<span class="eyebrow">Privacidade e LGPD</span><h1>Política de Privacidade</h1><p class="lead">Última atualização: 07/10/2026</p></div></section>
<section class="blk"><div class="wrap legal-doc">
<h2>1. Informações gerais</h2>
<p>A CMG Engenharia &amp; Consultoria, com sede na Avenida Del Rey, 111 - Sala 101 C, Bairro Caiçara, Belo Horizonte / MG - CEP: 30775-240, está comprometida com a proteção da privacidade e dos dados pessoais de seus clientes, visitantes do site e usuários de nossos serviços.</p>
<p>Esta Política de Privacidade descreve como coletamos, usamos, armazenamos e protegemos suas informações pessoais, em conformidade com a Lei Geral de Proteção de Dados (LGPD) - Lei nº 13.709/2018.</p>
<h2>2. Dados coletados</h2><p>Coletamos os seguintes tipos de informações:</p>
{ul(["Dados de identificação: nome completo, CPF/CNPJ, RG","Dados de contato: e-mail, telefone, endereço","Dados profissionais: empresa, cargo, área de atuação","Dados do projeto: informações técnicas sobre projetos solicitados","Dados de navegação: cookies, logs de acesso, endereço IP"])}
<h2>3. Finalidade do tratamento</h2><p>Utilizamos seus dados pessoais para:</p>
{ul(["Prestação de serviços de engenharia e consultoria","Elaboração de orçamentos e propostas comerciais","Comunicação sobre projetos e serviços","Cumprimento de obrigações legais e regulamentares","Melhoria de nossos serviços e experiência do usuário","Marketing direto (com seu consentimento)"])}
<h2>4. Base legal</h2><p>O tratamento de seus dados pessoais é fundamentado nas seguintes bases legais:</p>
{ul(["Execução de contrato ou procedimentos preliminares","Cumprimento de obrigação legal ou regulatória","Legítimo interesse da empresa","Consentimento do titular (quando aplicável)"])}
<h2>5. Compartilhamento de dados</h2><p>Seus dados pessoais podem ser compartilhados com:</p>
{ul(["Parceiros técnicos e fornecedores necessários para execução dos projetos","Órgãos públicos, quando exigido por lei","Prestadores de serviços (contabilidade, advocacia, TI)","Autoridades competentes, mediante ordem judicial"])}
<h2>6. Segurança dos dados</h2><p>Implementamos medidas técnicas e organizacionais adequadas para proteger seus dados pessoais contra acesso não autorizado, alteração, divulgação ou destruição, incluindo:</p>
{ul(["Criptografia de dados sensíveis","Controle de acesso restrito","Backup regular dos dados","Treinamento de funcionários","Monitoramento contínuo de segurança"])}
<h2>7. Retenção de dados</h2><p>Mantemos seus dados pessoais pelo tempo necessário para cumprir as finalidades descritas nesta política, respeitando os prazos legais aplicáveis:</p>
{ul(["Dados contratuais: 5 anos após o término do contrato","Dados fiscais: conforme legislação tributária","Dados de marketing: até a revogação do consentimento"])}
<h2>8. Seus direitos</h2><p>Você tem os seguintes direitos em relação aos seus dados pessoais:</p>
{ul(["Confirmação da existência de tratamento","Acesso aos dados","Correção de dados incompletos, inexatos ou desatualizados","Anonimização, bloqueio ou eliminação de dados desnecessários","Portabilidade dos dados","Eliminação dos dados tratados com consentimento","Revogação do consentimento"])}
<h2>9. Cookies</h2><p>Nosso site utiliza cookies para melhorar sua experiência de navegação. Os cookies são pequenos arquivos de texto armazenados em seu dispositivo que nos ajudam a:</p>
{ul(["Lembrar suas preferências","Analisar o tráfego do site","Personalizar conteúdo","Melhorar a funcionalidade do site"])}
<h2>10. Alterações na política</h2><p>Esta Política de Privacidade pode ser atualizada periodicamente. Recomendamos que você a revise regularmente. As alterações entrarão em vigor na data de sua publicação.</p>
<h2>11. Contato</h2><p>Para exercer seus direitos ou esclarecer dúvidas sobre esta Política de Privacidade, entre em contato conosco:</p>
{ul(["E-mail: carla@cmgenge.com.br","Telefone: (31) 98866-0712","Endereço: Avenida Del Rey, 111 - Sala 101 C, Bairro Caiçara, Belo Horizonte / MG - CEP: 30775-240"])}
<p style="margin-top:32px"><a class="back" href="index.html#contato">← Voltar para Contato</a></p>
</div></section>
'''
page = head("Política de Privacidade | CMG Engenharia & Consultoria", "Política de Privacidade e proteção de dados (LGPD) da CMG Engenharia & Consultoria.", "") + header("") + priv + footer("")
open(os.path.join(ROOT, "politica-de-privacidade.html"), "w", encoding="utf8").write(page)
exec(open(os.path.join(ROOT, '_build', 'blog.py'), encoding='utf8').read())
# ---------- 7) CSS: junta e minifica (menos requisicoes e menos bytes) ----------
def minify(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    return css.replace(';}', '}').strip()

def bundle(name, files):
    src = ''.join(open(os.path.join(ROOT, 'assets', 'css', f), encoding='utf8').read() + '\n' for f in files)
    out = minify(src)
    open(os.path.join(ROOT, 'assets', 'css', name), 'w', encoding='utf8').write(out)
    return len(src.encode('utf8')), len(out.encode('utf8'))

home_sz = bundle('home.min.css', ['site.css', 'menu.css', 'tap.css', 'fixes.css'])
pages_sz = bundle('pages.min.css', ['site.css', 'pages.css', 'menu.css', 'tap.css', 'servicos-mobile.css', 'servico-mobile.css', 'blog.css', 'fixes.css'])
print('CSS home %d -> %d bytes | paginas %d -> %d bytes' % (home_sz + pages_sz))

# a home usa um unico arquivo de CSS
hp = os.path.join(ROOT, 'index.html')
hs = open(hp, encoding='utf8').read()
hs2 = re.sub(r'(?:<link rel="stylesheet" href="assets/css/(?:site|menu|tap|home\.min)\.css(?:\?v=\d+)?">\n?)+', '<link rel="stylesheet" href="assets/css/home.min.css?v=%s">\n' % VER, hs, count=1)
hs2 = re.sub(r'assets/js/nav\.js(?:\?v=\d+)?', 'assets/js/nav.js?v=%s' % VER, hs2)
if hs2 != hs:
    open(hp, 'w', encoding='utf8').write(hs2)

print("paginas geradas:", len(S) + 2)
