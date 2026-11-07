#!/usr/bin/env python3
"""Confere o roteiro.json de um reel de curiosidade antes do storyboard.

Uso:  python3 ferramentas/gancho_check.py <pasta-do-reel>   (lê <pasta>/roteiro.json, fatos.md e pie.txt)
Sai com código 1 se houver ERRO. AVISO não bloqueia, mas pede um olhar.

Testa o que dá para testar sozinho: como cada gancho começa (data, lugar, ressalva, tom de notícia, anúncio,
"eu", clichê, plataforma), os 4 ganchos com formas diferentes, a frase 2, duração por palavras, chave de cada
frase, cena de cada bloco, número com fonte no fatos.md, fecho e texto do post. O resto (o estranho vem
primeiro? deixa pergunta? funciona sem som?) é olho humano: o script lembra no fim.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

PALAVRAS_POR_SEG = 2.7
FORMAS = {"contrario", "objeto", "numero", "pessoal", "pergunta"}
TIPOS_BOCETO = {"objeto", "cifra", "comparar", "lista", "dentro", "celular"}

# começo proibido (primeiras palavras do gancho), por idioma
INICIO = {
    "pt": [
        (r"^(em|no|na|nos|nas)\s+\d{3,4}\b", "começa com data"),
        (r"^h[aá]\s+(mais\s+de\s+)?\d+\s+(anos|dias|meses|s[eé]culos)", "começa com 'há X anos'"),
        (r"^(em|no|na)\s+(um|uma)\s+(cidade|vila|pa[ií]s|lugar|pequen)", "começa com lugar"),
        (r"^(segundo|de acordo|dizem|pelo visto|parece que|um estudo|uma pesquisa|pesquisadores|cientistas)\b", "começa com ressalva"),
        (r"^(hoje|neste v[ií]deo|no v[ií]deo de hoje|presta aten|aten[cç][aã]o|ol[aá]|oi|fala,? galera|bem-vindo|vou te|vou explicar|eu vou)\b", "anuncia em vez de intrigar"),
        (r"^voc[eê] sabia\b", "clichê 'você sabia'"),
        (r"^(um|uma) d[oa]s (maiores|mais)\b", "clichê 'um dos maiores'"),
    ],
    "es": [
        (r"^(en|el)\s+\d{3,4}\b", "empieza con fecha"),
        (r"^hace\s+\d+\s+(años|días|meses|siglos)", "empieza con 'hace X años'"),
        (r"^(según|de acuerdo|dicen|por lo visto|un estudio|investigadores|científicos)\b", "empieza con matiz"),
        (r"^(hoy|en este v[ií]deo|en el v[ií]deo de hoy|atento|atenci[oó]n|hola|bienvenid|te voy|voy a)\b", "anuncia en vez de intrigar"),
        (r"^¿?sab[ií]as que\b", "cliché '¿sabías que?'"),
        (r"^(uno|una) de los (mayores|más)\b", "cliché 'uno de los mayores'"),
    ],
    "en": [
        (r"^(in|on)\s+\d{3,4}\b", "starts with a date"),
        (r"^\d+\s+years ago", "starts with 'X years ago'"),
        (r"^(according|they say|apparently|a study|researchers|scientists)\b", "starts with a hedge"),
        (r"^(today|in this video|in today'?s video|pay attention|hey|hi|hello|welcome|i'?m going to|let me)\b", "announces instead of intriguing"),
        (r"^did you know\b", "cliché 'did you know'"),
        (r"^one of the (biggest|most)\b", "cliché 'one of the biggest'"),
    ],
}
# em qualquer lugar do gancho
DENTRO = {
    "pt": [
        (r"\b(acaba de|anunciou|lan[cç]ou|confirmou|divulgou)\b", "tom de notícia"),
        (r"\b(meu canal|meu perfil|aqui no (canal|perfil)|eu)\b", "fala de quem faz o vídeo"),
        (r"\b(algoritmo|intelig[eê]ncia artificial|chatgpt|\bia\b)\b", "fala da plataforma/ferramenta"),
        (r"\b(porque|por causa|[eé] que)\b", "parece já responder a pergunta"),
    ],
    "es": [
        (r"\b(acaba de|anunci[oó]|lanz[oó]|confirm[oó])\b", "tono de noticia"),
        (r"\b(mi canal|mi perfil|yo)\b", "habla de quien hace el vídeo"),
        (r"\b(algoritmo|inteligencia artificial|chatgpt|\bia\b)\b", "habla de la plataforma"),
        (r"\b(porque|por culpa de|es que)\b", "parece contestar la pregunta"),
    ],
    "en": [
        (r"\b(just launched|announced|confirmed|unveiled)\b", "news tone"),
        (r"\b(my channel|my page|i)\b", "talks about the creator"),
        (r"\b(algorithm|artificial intelligence|chatgpt|\bai\b)\b", "talks about the platform"),
        (r"\b(because|that'?s why)\b", "seems to answer the question"),
    ],
}
SEGUNDA_PESSOA = {"pt": r"\b(voc[eê]|seu|sua|seus|suas|te|teu|tua)\b",
                  "es": r"\b(t[uú]|te|tu|tus|usted|su)\b",
                  "en": r"\b(you|your)\b"}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def palavras(t):
    return re.findall(r"[\wÀ-ÿ%°,.]+", t)


def checar(pasta: Path):
    erros, avisos = [], []
    rp = pasta / "roteiro.json"
    if not rp.exists():
        return [f"falta {rp}"], []
    try:
        r = json.loads(rp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"roteiro.json inválido: {e}"], []
    lang = r.get("idioma", "pt")
    if lang not in INICIO:
        erros.append(f"idioma '{lang}' sem regras (use pt, es ou en)")
        lang = "pt"

    # ---- ganchos
    g = r.get("gancho") or {}
    reserva = r.get("reserva") or []
    todos = [("gancho", g)] + [(f"reserva[{i}]", x) for i, x in enumerate(reserva)]
    if not g.get("texto"):
        erros.append("falta gancho.texto")
    if len(reserva) != 3:
        erros.append(f"escreva 4 ganchos: 1 em 'gancho' + 3 em 'reserva' (tem {len(reserva)} na reserva)")
    formas = []
    for nome, h in todos:
        t = (h.get("texto") or "").strip()
        if not t:
            continue
        low = t.lower()
        for pad, msg in INICIO[lang]:
            if re.search(pad, low):
                erros.append(f"{nome}: {msg} — \"{t}\"")
        for pad, msg in DENTRO[lang]:
            if re.search(pad, low):
                (avisos if "responder" in msg or "contestar" in msg or "answer" in msg else erros).append(
                    f"{nome}: {msg} — \"{t}\"")
        n = len(palavras(t))
        if n > 14:
            avisos.append(f"{nome}: {n} palavras — entende de primeira, em voz alta?")
        if not re.search(SEGUNDA_PESSOA[lang], low) and h.get("forma") not in ("objeto", "numero"):
            avisos.append(f"{nome}: não fala com a pessoa (você/seu) nem é forma 'objeto'/'numero' — é algo dela?")
        if not h.get("imagem"):
            erros.append(f"{nome}: falta 'imagem' (o que enche o quadro 0 e o que se mexe)")
        f = h.get("forma")
        if f not in FORMAS:
            erros.append(f"{nome}: forma '{f}' inválida (use {', '.join(sorted(FORMAS))})")
        formas.append(f)
    if len([f for f in formas if f]) == 4 and len(set(formas)) < 4:
        erros.append(f"os 4 ganchos repetem forma ({', '.join(formas)}): cada um com uma forma diferente")

    # ---- blocos
    blocos = r.get("blocos") or []
    if not blocos:
        erros.append("faltam blocos")
        return erros, avisos
    frases = [f for b in blocos for f in b.get("frases", [])]
    if g.get("texto") and frases and frases[0].get("texto", "").strip() != g["texto"].strip():
        erros.append("a 1ª frase do bloco b0 tem de ser o gancho escolhido (igual a gancho.texto)")
    if len(frases) < 2:
        erros.append("falta a frase 2 (descarta o que a pessoa já está pensando ou diz a pergunta)")
    cenas = r.get("cenas") or {}
    for b in blocos:
        c = b.get("cena")
        if not c:
            erros.append(f"bloco {b.get('id')}: sem 'cena'")
        elif c not in cenas:
            erros.append(f"bloco {b.get('id')}: cena '{c}' não está em 'cenas'")
    for nome, c in cenas.items():
        if not c.get("que"):
            erros.append(f"cena {nome}: falta 'que' (o que se vê e o que se mexe)")
        bt = (c.get("boceto") or {}).get("tipo")
        if bt not in TIPOS_BOCETO:
            erros.append(f"cena {nome}: boceto.tipo '{bt}' inválido (use {', '.join(sorted(TIPOS_BOCETO))})")
    for f in frases:
        ch = f.get("chave")
        if ch and sem_acento(ch.lower()) not in sem_acento(f.get("texto", "").lower()):
            erros.append(f"frase {f.get('id')}: chave '{ch}' não está no texto")
    if sum(1 for f in frases if f.get("chave")) < len(frases) * 0.6:
        avisos.append("menos de 60% das frases têm 'chave': lidas em sequência, as chaves deveriam contar o vídeo")

    # ---- duração
    total = sum(len(palavras(f.get("texto", ""))) for f in frases)
    seg = total / PALAVRAS_POR_SEG
    alvo = r.get("duracao")
    if alvo:
        if seg > alvo * 1.25:
            erros.append(f"{total} palavras ≈ {seg:.0f} s, passa muito dos {alvo} s pedidos: corte frases que sobram")
        elif seg < alvo * 0.6:
            avisos.append(f"{total} palavras ≈ {seg:.0f} s, bem menos que {alvo} s (tudo bem se a história acabou)")

    # ---- fecho
    fecho = (r.get("fecho") or "").strip()
    if not fecho:
        erros.append("falta 'fecho' (o fecho fixo da conta)")
    elif frases and fecho not in frases[-1].get("texto", ""):
        erros.append("a última frase tem de trazer o fecho")

    # ---- números com fonte
    fatos = pasta / "fatos.md"
    nums = set()
    for f in frases:
        nums |= set(re.findall(r"\d+(?:[.,]\d+)?", f.get("texto", "")))
    for v in (r.get("tela") or {}).values():
        nums |= set(re.findall(r"\d+(?:[.,]\d+)?", str(v)))
    if not fatos.exists():
        erros.append("falta fatos.md (cada número com fonte e a frase exata)")
    else:
        ft = fatos.read_text(encoding="utf-8")
        if "http" not in ft:
            erros.append("fatos.md sem nenhum link de fonte")
        for n in sorted(nums):
            if n not in ft:
                erros.append(f"número {n} do roteiro não está no fatos.md")

    # ---- texto do post
    pie = pasta / "pie.txt"
    if not pie.exists():
        erros.append("falta pie.txt (texto do post)")
    else:
        pt = pie.read_text(encoding="utf-8").strip()
        if "#" in pt:
            erros.append("pie.txt: sem hashtag")
        if "—" in pt:
            erros.append("pie.txt: sem travessão longo")
        if pt and len(pt.splitlines()[0]) > 120:
            avisos.append("pie.txt: a 1ª linha passa de 120 caracteres")
    return erros, avisos


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help", "--ajuda"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    erros, avisos = checar(Path(sys.argv[1]))
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("AVISO ", a)
    print("\nOlho humano (o script não vê): o estranho vem primeiro? deixa uma pergunta? o quadro 0 mostra o gancho "
          "sem som? compare os 4 ganchos de dois em dois.")
    print("OK" if not erros else f"\n{len(erros)} erro(s): reescreva e rode de novo.")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
