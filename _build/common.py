# -*- coding: utf-8 -*-
"""Menu de navegacao compartilhado (home e paginas internas)."""

GROUPS = [
    ("Projetos Complementares", [
        ("Estrutura de Concreto e Alvenaria", "estrutura-concreto-alvenaria"),
        ("Instalações Hidrossanitárias", "instalacoes-hidrossanitarias"),
        ("Instalações Elétricas de Baixa Tensão", "instalacoes-eletricas-baixa-tensao"),
    ]),
    ("Vistoria e Perícia", [
        ("Vistoria de Reforma", "vistoria-de-reforma"),
        ("Vistoria Cautelar", "vistoria-cautelar"),
        ("Vistoria de Entrega de Imóvel", "vistoria-de-entrega-de-imovel"),
        ("Vistoria de Atendimento à NBR 15575", "vistoria-nbr-15575"),
        ("Inspeção Predial", "inspecao-predial"),
        ("Perícia Estrutural e Análise de Patologias", "pericia-estrutural"),
    ]),
]


def nav_html(R, home=False):
    """R = prefixo ate a raiz ('' na home, '../' em servicos/)."""
    base = R + "servicos/"
    idx = base + "index.html"
    h_home = "#inicio" if home else R + "index.html"
    h_sobre = "#sobre" if home else R + "index.html#sobre"
    h_cont = "#contato" if home else R + "index.html#contato"
    subs = ""
    for title, items in GROUPS:
        links = "".join(f'<a href="{base}{slug}.html">{t}</a>' for t, slug in items)
        subs += (f'<div class="dd-s"><button type="button" class="dd-t" aria-haspopup="true" aria-expanded="false">{title}</button>'
                 f'<div class="dd-sp"><div class="dd-sin">{links}</div></div></div>')
    return f'''
      <a class="lnk" href="{h_home}">Home</a>
      <a class="lnk" href="{h_sobre}">Sobre</a>
      <div class="dd"><a class="lnk" href="{idx}">Serviços<i class="chev" aria-hidden="true"></i></a><div class="dd-p"><div class="dd-in">{subs}<a class="dd-t" href="{base}engenharia-social.html">Engenharia Social</a><a class="dd-all" href="{idx}">Ver Todos os Serviços</a></div></div></div>
      <a class="lnk" href="{R}blog/index.html">Blog</a>
      <a class="lnk" href="{h_cont}">Contato</a>
      <a class="btn btn-primary" href="{h_cont}">Solicitar orçamento</a>
      <div class="nav-foot"><a href="tel:+5531988660712">(31) 98866-0712</a><a href="https://wa.me/5531988660712?text=Ol%C3%A1%2C%20gostaria%20de%20solicitar%20um%20or%C3%A7amento." target="_blank" rel="noopener">WhatsApp</a><span>Seg a sex · 8h às 18h</span></div>
    '''
