# -*- coding: utf-8 -*-
"""Blog: gera blog/index.html e um arquivo por artigo. Executado de dentro do build.py (usa head/header/footer/crumbs/cta_band).
Para publicar um artigo novo: acrescente um item em POSTS e rode o build.py de novo."""
import os

# Artigos de exemplo (nao publicados). Para publicar um, copie o item para POSTS.
EXEMPLOS = [
    {"slug": "fissuras-em-paredes-quando-se-preocupar", "data": "23/11/2026", "iso": "2026-11-23", "min": 4,
     "cat": "Patologias",
     "img": ("cautelar.webp", "Engenheira analisando uma fissura em parede"),
     "titulo": "Fissuras em paredes: quando é só estética e quando é sinal de alerta",
     "resumo": "Nem toda fissura é perigosa, mas algumas pedem avaliação técnica rápida. Veja como diferenciar.",
     "corpo": [
        ("h2", "Fissura, trinca, rachadura: qual a diferença?"),
        ("p", "Em engenharia, o que muda o nome é a abertura. Fissuras são muito finas, trincas são mais largas e rachaduras já permitem ver através da parede. Quanto maior a abertura, maior a chance de a causa ser estrutural."),
        ("h2", "Sinais que costumam ser apenas estéticos"),
        ("ul", ["Fissuras muito finas, em linhas curtas, no encontro entre parede e laje ou entre parede e viga;", "Fissuras que aparecem logo após a obra e não crescem com o tempo;", "Pequenos descolamentos de pintura ou de reboco sem abertura na alvenaria."]),
        ("h2", "Sinais que pedem avaliação técnica"),
        ("ul", ["Fissuras inclinadas a cerca de 45 graus, principalmente perto de portas e janelas;", "Aberturas que aumentam com o passar das semanas;", "Portas e janelas que passaram a emperrar;", "Desnível no piso ou paredes que parecem ter saído do prumo;", "Fissuras acompanhadas de umidade, ferrugem ou lascamento do concreto."]),
        ("h2", "O que fazer ao notar uma fissura"),
        ("p", "Fotografe a fissura com uma régua ou uma moeda ao lado, anote a data e acompanhe se ela cresce. Evite apenas rebocar por cima: sem entender a causa, a fissura volta. Uma vistoria feita por engenheiro identifica a origem e indica a solução correta."),
        ("p", "Cada caso é único. Este texto é informativo e não substitui a avaliação técnica no local."),
     ]},
    {"slug": "vistoria-cautelar-por-que-fazer-antes-de-uma-obra", "data": "23/11/2026", "iso": "2026-11-23", "min": 4,
     "cat": "Vistoria",
     "img": ("inspecao.webp", "Inspeção de uma edificação vizinha a uma obra"),
     "titulo": "Vistoria cautelar: por que fazer antes de uma obra vizinha",
     "resumo": "O laudo registra o estado do imóvel antes da obra e protege tanto quem constrói quanto quem mora ao lado.",
     "corpo": [
        ("h2", "O que é a vistoria cautelar"),
        ("p", "É uma inspeção técnica, com registro fotográfico e descrição detalhada, do estado de uma edificação antes do início de uma obra próxima. O laudo funciona como retrato do imóvel naquele momento."),
        ("h2", "Por que ela protege os dois lados"),
        ("ul", ["Para o vizinho, comprova quais danos já existiam e quais surgiram depois;", "Para quem constrói, evita questionamentos sem prova e reduz o risco de disputas;", "Para ambos, facilita acordos, porque o debate parte de fatos documentados."]),
        ("h2", "Quando faz sentido contratar"),
        ("ul", ["Antes de escavações, demolições, estacas ou obras de grande porte ao lado;", "Quando o seu imóvel é antigo ou já tem fissuras conhecidas;", "Quando a obra é sua e há edificações próximas."]),
        ("h2", "O que o laudo traz"),
        ("p", "Descrição dos ambientes, fotos datadas das fissuras, manchas e demais patologias existentes, além da assinatura de engenheiro com responsabilidade técnica. Se houver reclamação no futuro, o laudo é a referência para comparar o antes e o depois."),
     ]},
    {"slug": "inspecao-predial-nbr-16747", "data": "23/11/2026", "iso": "2026-11-23", "min": 4,
     "cat": "Inspeção predial",
     "img": ("s-desempenho.webp", "Fachada de edifício em inspeção predial"),
     "titulo": "Inspeção predial e a NBR 16747: o que o condomínio precisa saber",
     "resumo": "A norma organiza a inspeção das edificações e ajuda a priorizar reparos antes que o problema fique caro.",
     "corpo": [
        ("h2", "O que a norma estabelece"),
        ("p", "A ABNT NBR 16747 define diretrizes, conceitos e procedimentos para a inspeção predial: como analisar a edificação, classificar as anomalias encontradas e indicar a ordem de prioridade das providências."),
        ("h2", "Para que serve na prática"),
        ("ul", ["Identificar problemas de estrutura, fachada, cobertura, instalações e impermeabilização;", "Classificar o que é urgente e o que pode ser planejado;", "Apoiar o plano de manutenção e o orçamento do condomínio."]),
        ("h2", "Quem deve se preocupar com isso"),
        ("p", "Condomínios, construtoras e proprietários de edificações de qualquer porte. Quanto mais antiga a construção, mais importante é a inspeção periódica. A manutenção preventiva costuma custar bem menos do que o reparo de um problema que se agravou."),
        ("h2", "O que esperar do relatório"),
        ("p", "O relatório descreve as anomalias, registra com fotos, sugere as ações e as prioriza. Com ele, síndico e moradores decidem com segurança o que fazer primeiro."),
     ]},
]

exec(open(os.path.join(ROOT, '_build', 'blog_md.py'), encoding='utf8').read())
POSTS = _load_posts()

def _corpo(items):
    out = []
    for t, v in items:
        if t == "h2": out.append(f"<h2>{e(v)}</h2>")
        elif t == "p": out.append(f"<p>{e(v)}</p>")
        elif t == "ul": out.append("<ul>" + "".join(f"<li>{e(i)}</li>" for i in v) + "</ul>")
    return "\n".join(out)

def _bcard(p, R):
    f, alt = p["img"]
    return (f'<a class="bcard" href="{R}{p["slug"]}.html"><div class="bc-im"><img src="../assets/img/{f}" alt="{e(alt)}" loading="lazy" width="1200" height="900"></div>'
            f'<div class="bc-b"><span class="bc-m"><b>{e(p["cat"])}</b> · {p["min"]} min</span><span class="bc-t">{e(p["titulo"])}</span>'
            f'<span class="bc-p">{e(p["resumo"])}</span><span class="bc-l">Ler artigo<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div></a>')

os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
for _f in os.listdir(os.path.join(ROOT, "blog")):
    if _f.endswith(".html"): os.remove(os.path.join(ROOT, "blog", _f))
RB = "../"
# ---- indice do blog ----
idx_html = head("Blog de Engenharia Civil | CMG Engenharia & Consultoria",
                "Artigos de engenharia civil em Belo Horizonte: fissuras, vistoria cautelar, inspeção predial, normas e cuidados com o imóvel.", RB)
idx_html += header(RB)
idx_html += (f'<section class="pg-hero compact"><div class="wrap">{crumbs([("Início", RB + "index.html"), ("Blog", None)])}'
             '<h1>Blog</h1><p class="lead">Conteúdo técnico, em linguagem simples, para cuidar bem do seu imóvel.</p></div></section>'
             '<section class="blk" style="padding-top:var(--s5)"><div class="wrap"><div class="bgrid">'
             + ("".join(_bcard(p, "") for p in POSTS) if POSTS else '<p class="blog-vazio">Em breve, novos artigos por aqui.</p>') + '</div></div></section>')
idx_html += cta_band(RB, "Olá, vi o blog da CMG e gostaria de solicitar um orçamento.") + footer(RB)
open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf8").write(idx_html)

# ---- artigos ----
for i, p in enumerate(POSTS):
    outros = [q for q in POSTS if q is not p][:2]
    f, alt = p["img"]
    h = head(p["titulo"] + " | CMG Engenharia", p["resumo"], RB)
    h += header(RB)
    h += (f'<section class="pg-hero compact"><div class="wrap">{crumbs([("Início", RB + "index.html"), ("Blog", "index.html"), (p["cat"], None)])}'
          f'<span class="eyebrow">{e(p["cat"])}</span><h1>{e(p["titulo"])}</h1>'
          f'<p class="lead">{p["data"]} · {p["min"]} min de leitura</p></div></section>')
    h += (f'<section class="blk"><div class="wrap"><article class="post"><img class="post-im" src="../assets/img/{f}" alt="{e(alt)}" width="1200" height="900">'
          f'<div class="legal-doc">{p["html"] if "html" in p else _corpo(p["corpo"])}<p class="post-by"><b>Carla Montanari</b> · Engenheira civil · CREA 60936/D</p></div></article>' +
          (('<h2 class="post-more">Leia também</h2><div class="bgrid">' + "".join(_bcard(q, "") for q in outros) + '</div>') if outros else '') + '</div></section>')
    h += cta_band(RB, "Olá, li um artigo no blog e gostaria de solicitar um orçamento.") + footer(RB)
    open(os.path.join(ROOT, "blog", p["slug"] + ".html"), "w", encoding="utf8").write(h)
print("blog:", len(POSTS), "artigos")
