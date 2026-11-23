# -*- coding: utf-8 -*-
"""Atualiza o menu da home com o nav de common.py (inclui o rodape do menu)
e carrega assets/css/menu.css na home. Rodar uma vez; depois: python -I _build/build.py"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from common import nav_html

p = os.path.join(ROOT, "index.html")
s = open(p, encoding="utf8").read()
s, n = re.subn(r'<nav class="main" id="nav">.*?</nav>',
               lambda m: '<nav class="main" id="nav">' + nav_html("", home=True) + '</nav>', s, count=1, flags=re.S)
assert n == 1
s = s.replace('<button class="burger" id="burger" aria-label="Abrir menu">',
              '<button class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav">')
if "assets/css/menu.css" not in s:
    s = s.replace('<link rel="stylesheet" href="assets/css/site.css">',
                  '<link rel="stylesheet" href="assets/css/site.css">\n<link rel="stylesheet" href="assets/css/menu.css">', 1)
open(p, "w", encoding="utf8").write(s)

# paginas internas: build.py passa a carregar menu.css tambem
bp = os.path.join(HERE, "build.py")
b = open(bp, encoding="utf8").read()
if "menu.css" not in b:
    old = '<link rel="stylesheet" href="{R}assets/css/pages.css">'
    assert old in b
    b = b.replace(old, old + '\n<link rel="stylesheet" href="{R}assets/css/menu.css">', 1)
    open(bp, "w", encoding="utf8").write(b)
print("menu atualizado")
