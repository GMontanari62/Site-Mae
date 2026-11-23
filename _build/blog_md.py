# -*- coding: utf-8 -*-
"""Le os artigos que a Carla escreve no painel (content/blog/*.md) e converte para HTML.
Executado de dentro do blog.py (usa ROOT, os e e = html.escape)."""
import re as _re, math as _math


def _inline(t):
    t = e(t)
    t = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = _re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = _re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+|tel:[^)\s]+)\)",
                r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return t


def _md(md):
    """Markdown simples (o que o painel oferece): ## titulo, ### subtitulo, listas, negrito, italico, links."""
    out, par, lst = [], [], []

    def flush():
        if par:
            out.append("<p>" + _inline(" ".join(par)) + "</p>")
            par.clear()
        if lst:
            out.append("<ul>" + "".join("<li>" + _inline(i) + "</li>" for i in lst) + "</ul>")
            lst.clear()

    for raw in md.replace("\r", "").split("\n"):
        ln = raw.strip()
        m = _re.match(r"^(#{1,4})\s+(.*)$", ln)
        b = _re.match(r"^[-*]\s+(.*)$", ln)
        if not ln:
            flush()
        elif m:
            flush()
            tag = "h2" if len(m.group(1)) <= 2 else "h3"
            out.append("<%s>%s</%s>" % (tag, e(m.group(2)), tag))
        elif b:
            if par:
                flush()
            lst.append(b.group(1))
        else:
            if lst:
                flush()
            par.append(ln)
    flush()
    return "\n".join(out)


def _unq(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        q = v[0]
        v = v[1:-1]
        v = v.replace('\\"', '"') if q == '"' else v.replace("''", "'")
    return v


def _load_posts():
    d = os.path.join(ROOT, "content", "blog")
    posts = []
    if not os.path.isdir(d):
        return posts
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        txt = open(os.path.join(d, fn), encoding="utf8").read().replace("\r", "")
        m = _re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, _re.S)
        if not m:
            continue
        fm = {}
        for ln in m.group(1).split("\n"):
            k, _, v = ln.partition(":")
            if k and not k.startswith(" "):
                fm[k.strip()] = _unq(v)
        if fm.get("publicado", "true").lower() == "false" or not fm.get("titulo"):
            continue
        body = m.group(2).strip()
        dt = (fm.get("data") or "")[:10]
        try:
            y, mo, da = dt.split("-")
            br = "%s/%s/%s" % (da, mo, y)
        except ValueError:
            dt, br = "", ""
        img = (fm.get("imagem") or "").lstrip("/")
        if img.startswith("assets/img/"):
            img = img[len("assets/img/"):]
        if not img:
            img = "projeto.webp"
        posts.append({"slug": fn[:-3], "data": br, "iso": dt, "min": max(1, _math.ceil(len(body.split()) / 200)),
                      "cat": fm.get("categoria") or "Blog", "img": (img, fm["titulo"]),
                      "titulo": fm["titulo"], "resumo": fm.get("resumo") or "", "html": _md(body)})
    posts.sort(key=lambda p: p["iso"], reverse=True)
    return posts
