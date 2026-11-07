#!/usr/bin/env python3
"""Cria a pasta de um reel novo com roteiro.json, fatos.md e pie.txt para preencher.

Uso:  python3 ferramentas/novo.py <slug> ["pergunta do reel"] [--duracao 30] [--idioma pt]
Cria exemplos/<slug>/ (não sobrescreve pasta que já existe).
"""
import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("pergunta", nargs="?", default="")
    ap.add_argument("--duracao", type=int, default=30)
    ap.add_argument("--idioma", default="pt", choices=["pt", "es", "en"])
    a = ap.parse_args()
    p = RAIZ / "exemplos" / a.slug
    if p.exists():
        sys.exit(f"{p} já existe: não sobrescrevo")
    p.mkdir(parents=True)
    pref = RAIZ / "preferencias.md"
    fecho = "Manda para quem sempre te pergunta isso."
    if pref.exists():
        for ln in pref.read_text(encoding="utf-8").splitlines():
            if ln.lower().startswith("fecho:"):
                fecho = ln.split(":", 1)[1].strip()
    r = {
        "id": a.slug, "idioma": a.idioma, "voz": "nei", "duracao": a.duracao,
        "pausa": 0.18, "intervalo_blocos": 0.3,
        "publico": "", "pergunta": a.pergunta,
        "gancho": {"texto": "", "forma": "", "imagem": ""},
        "reserva": [{"texto": "", "forma": "", "imagem": ""} for _ in range(3)],
        "fecho": fecho,
        "tela": {}, "destaques": [],
        "blocos": [{"id": "b0", "cena": "gancho", "frases": [{"id": "g", "texto": "", "chave": ""}]}],
        "cenas": {"gancho": {"entrada": "corte", "que": "", "boceto": {"tipo": "objeto", "texto": ""}, "som": ""}},
    }
    (p / "roteiro.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    (p / "fatos.md").write_text(f"# Fatos — {a.slug}\n\nCada número: valor · frase exata da fonte · link · conferido em AAAA-MM-DD.\n"
                                "Sem fonte, fica de fora.\n\n", encoding="utf-8")
    (p / "pie.txt").write_text("", encoding="utf-8")
    print(p)
    print("Próximo: fatos.md → 4 ganchos → blocos e cenas → python3 ferramentas/gancho_check.py", p)


if __name__ == "__main__":
    main()
