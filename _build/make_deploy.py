# -*- coding: utf-8 -*-
"""Monta a pasta limpa para publicar (Netlify): so o que o site realmente usa.
Uso (a partir de cmg-engenharia):  python -I _build/build.py && python -I _build/make_deploy.py
Saida: ../cmg-engenharia-netlify"""
import os, re, shutil
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("DEPLOY_OUT") or os.path.join(os.path.dirname(ROOT), "cmg-engenharia-netlify")
os.makedirs(OUT, exist_ok=True)

htmls = [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "politica-de-privacidade.html")]
htmls += [os.path.join(ROOT, "blog", f) for f in sorted(os.listdir(os.path.join(ROOT, "blog"))) if f.endswith(".html")]
htmls += [os.path.join(ROOT, "servicos", f) for f in sorted(os.listdir(os.path.join(ROOT, "servicos"))) if f.endswith(".html")]

refs = set()
pat = re.compile(r'assets/[^"\'\s)?#]+')
for h in htmls:
    for m in pat.finditer(open(h, encoding="utf8").read()):
        refs.add(m.group(0))

copiados, faltando = [], []
def copia(rel):
    rel = unquote(rel)
    src = os.path.join(ROOT, rel)
    dst = os.path.join(OUT, rel)
    if not os.path.exists(src):
        faltando.append(rel); return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst); copiados.append(rel)

for h in htmls:
    copia(os.path.relpath(h, ROOT))
for r in sorted(refs):
    copia(r)
for extra in ("robots.txt", "_headers", "assets/video/hero-m.mp4", "assets/video/cena2-m.mp4"):
    copia(extra)

# fotos enviadas pelo painel (nomes podem ter espaco, que a busca por links nao pega)
_bd = os.path.join(ROOT, "assets", "img", "blog")
if os.path.isdir(_bd):
    for _f in os.listdir(_bd):
        copia("assets/img/blog/" + _f)

# painel de edicao do blog (/admin)
for _f in os.listdir(os.path.join(ROOT, "admin")):
    copia("admin/" + _f)

total = sum(os.path.getsize(os.path.join(OUT, c)) for c in copiados)
mb = lambda b: round(b / 1048576, 1)
videos = sum(os.path.getsize(os.path.join(OUT, c)) for c in copiados if c.endswith(".mp4"))
print("pasta:", OUT)
print("arquivos:", len(copiados), "| tamanho total:", mb(total), "MB (videos:", mb(videos), "MB)")
if faltando:
    print("ATENCAO, referenciados mas inexistentes:", faltando)
