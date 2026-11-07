#!/usr/bin/env python3
"""Curio — o agente da conta. Separa as mensagens e comentários e PROPÕE respostas. Não envia nada.

Uso:  python3 agentes/curio_triagem.py <mensagens.json> --link <url> [--estado estado.json] [--json]

mensagens.json: [{"id": "m1", "de": "@ana", "onde": "dm|comentario", "texto": "como você fez esse vídeo?"}]

O que faz:
  - "como faz?" / "qual app?" / "me ensina"  → resposta pronta com o link etiquetado (você revisa e envia);
  - queixa, reembolso, marca/parceria        → vai para você, sem resposta automática;
  - elogio                                    → curtir (sugestão);
  - o resto                                   → ignora.
Com --estado, lembra quais ids já viu e só avisa quando há NOVIDADE (pensado para rodar 4×/dia).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

CLASSES = [
    ("reembolso", r"reembols|estorn|devolu|devolv|cancelar (a )?compra|meu dinheiro|refund|chargeback"),
    ("queixa", r"nao funciona|não funciona|golpe|fraude|enganad|pessim|péssim|horrivel|horrível|reclam|denunci|scam"),
    ("marca", r"parceria|publi\b|publipost|collab|patrocin|orcamento|orçamento|media ?kit|sou da marca|agencia|agência"),
    ("como_faz", r"como (voce|você|vc|tu)? ?(fez|faz|faco|faço|cria|criou)|qual (app|programa|ia|ferramenta|site)|"
                 r"me ensina|tutorial|passo a passo|link|onde (aprendo|compro|acho)|quero fazer|como se faz|ensina"),
    ("elogio", r"incr[ií]vel|amei|top\b|sensacional|muito bom|que legal|perfeito|show\b|parab[eé]ns|😍|🔥|👏"),
]
PARA_DONO = {"reembolso", "queixa", "marca"}


def norm(s):
    s = unicodedata.normalize("NFC", s.lower())
    return s


def classificar(texto: str) -> str:
    t = norm(texto)
    for nome, pad in CLASSES:
        if re.search(pad, t):
            return nome
    return "outro"


def resposta(classe: str, link: str, nome: str = "") -> str:
    if classe == "como_faz":
        return (f"Oi{(' ' + nome) if nome else ''}! Eu explico o passo a passo inteiro, de graça, aqui: {link} "
                "Qualquer dúvida, me chama.")
    if classe == "elogio":
        return "(curtir o comentário)"
    return ""


def triar(msgs, link, vistos=None):
    vistos = set(vistos or [])
    novos = [m for m in msgs if m.get("id") not in vistos]
    itens = []
    for m in novos:
        c = classificar(m.get("texto", ""))
        if c == "outro":
            continue
        itens.append({"id": m.get("id"), "de": m.get("de", ""), "onde": m.get("onde", ""), "classe": c,
                      "texto": m.get("texto", ""), "proposta": resposta(c, link, m.get("de", "").lstrip("@")),
                      "para_dono": c in PARA_DONO})
    cont = {}
    for i in itens:
        cont[i["classe"]] = cont.get(i["classe"], 0) + 1
    tem_novidade = bool(itens)
    return {"novidade": tem_novidade, "contagem": cont, "itens": itens,
            "vistos": sorted(vistos | {m.get("id") for m in msgs}), "envia": False}


def texto(r):
    if not r["novidade"]:
        return "Curio: nada novo."
    out = ["Curio · novidades da conta (nada foi enviado)", ""]
    dono = [i for i in r["itens"] if i["para_dono"]]
    if dono:
        out.append("Para você decidir:")
        for i in dono:
            out.append(f"  [{i['classe']}] {i['de']} ({i['onde']}): {i['texto']}")
        out.append("")
    cf = [i for i in r["itens"] if i["classe"] == "como_faz"]
    if cf:
        out.append(f"{len(cf)} perguntaram como faz. Respostas propostas (responda 'ok' para enviar todas):")
        for i in cf:
            out.append(f"  {i['de']} ({i['onde']}): {i['proposta']}")
    el = sum(1 for i in r["itens"] if i["classe"] == "elogio")
    if el:
        out.append(f"{el} elogio(s): curtir.")
    return "\n".join(out)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "--ajuda"):
        print(__doc__)
        sys.exit(0)
    link = a[a.index("--link") + 1] if "--link" in a else "https://inema.club"
    est = Path(a[a.index("--estado") + 1]) if "--estado" in a else None
    vistos = json.loads(est.read_text())["vistos"] if est and est.exists() else []
    r = triar(json.load(open(a[0], encoding="utf-8")), link, vistos)
    if est:
        est.write_text(json.dumps({"vistos": r["vistos"]}), encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in a else texto(r))


if __name__ == "__main__":
    main()
