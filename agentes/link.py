#!/usr/bin/env python3
"""Link etiquetado: cada reel, a bio e cada resposta ganham um link próprio, para saber de onde veio a pessoa.

Uso:  python3 agentes/link.py <url> --conta <nome> --onde reel|bio|dm|anuncio [--reel <slug>]
Ex.:  python3 agentes/link.py https://inema.club --conta curiosidade --onde reel --reel geladeira
      → https://inema.club/?utm_source=instagram&utm_medium=reel&utm_campaign=curiosidade&utm_content=geladeira
"""
import argparse
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

ONDE = {"reel", "bio", "dm", "anuncio", "comentario"}


def etiquetar(url, conta, onde, reel="", rede="instagram"):
    if onde not in ONDE:
        raise ValueError(f"onde = {', '.join(sorted(ONDE))}")
    u = urlparse(url)
    q = dict(parse_qsl(u.query))
    q.update({"utm_source": rede, "utm_medium": onde, "utm_campaign": conta})
    if reel:
        q["utm_content"] = reel
    return urlunparse(u._replace(path=u.path or "/", query=urlencode(q)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--conta", required=True)
    ap.add_argument("--onde", required=True)
    ap.add_argument("--reel", default="")
    ap.add_argument("--rede", default="instagram")
    a = ap.parse_args()
    print(etiquetar(a.url, a.conta, a.onde, a.reel, a.rede))


if __name__ == "__main__":
    main()
