#!/usr/bin/env python3
"""Clic — o agente dos anúncios. Lê as métricas e PROPÕE. Nunca executa nada.

Uso:  python3 agentes/clic_regras.py <metricas.json> [--json]

As 4 regras (no código, não no prompt):
  1. Sem OK não gasta: a saída é só proposta; quem liga, sobe ou pausa é o dono.
  2. Teto por dia: a soma do orçamento diário proposto nunca passa de `teto_dia`.
  3. Só sobe o que vende: aumenta só com retorno (receita ÷ gasto) ≥ `retorno_min` e pelo menos 1 venda.
  4. Corta rápido: anúncio que já gastou `gasto_corte` sem nenhuma venda → cortar e trocar por outro.
E dois alarmes do caso real: medição quebrada (sem medir, nada sobe) e verba espalhada (muitos anúncios com
pouca verba não aprendem: concentre).

metricas.json:
{
  "config": {"teto_dia": 150, "retorno_min": 1.5, "gasto_corte": 30, "passo": 0.25, "min_por_anuncio": 10},
  "medicao_ok": true,
  "compradores_excluidos": true,
  "anuncios": [
    {"id": "A1", "orcamento_dia": 30, "gasto": 64, "vendas": 4, "receita": 156}
  ]
}
Moeda: tudo na mesma moeda (converta antes, se a loja e a rede usam moedas diferentes).
"""
import json
import sys

PADRAO = {"teto_dia": 150.0, "retorno_min": 1.5, "gasto_corte": 30.0, "passo": 0.25, "min_por_anuncio": 10.0}


def propor(m: dict) -> dict:
    cfg = {**PADRAO, **(m.get("config") or {})}
    ads = [dict(a) for a in m.get("anuncios", [])]
    props, alertas = [], []
    medicao = m.get("medicao_ok", True)
    if not medicao:
        alertas.append("MEDIÇÃO QUEBRADA: sem saber de onde vem a venda, nada sobe. Conserte a medição antes de "
                       "gastar mais (no caso real, um dia sem medir: 19 abriram o pagamento e 0 compraram).")
    if not m.get("compradores_excluidos", True):
        alertas.append("Quem já comprou ainda vê o anúncio: exclua os compradores do público.")

    ativos = [a for a in ads if a.get("orcamento_dia", 0) > 0]
    pequenos = [a for a in ativos if a["orcamento_dia"] < cfg["min_por_anuncio"]]
    if len(ativos) >= 4 and len(pequenos) >= len(ativos) / 2:
        alertas.append(f"Verba espalhada: {len(pequenos)} de {len(ativos)} anúncios com menos de "
                       f"{cfg['min_por_anuncio']:g}/dia. Concentre a verba nos que já vendem.")

    novo = {}
    for a in ads:
        orc = float(a.get("orcamento_dia", 0))
        gasto, vendas, receita = float(a.get("gasto", 0)), int(a.get("vendas", 0)), float(a.get("receita", 0))
        ret = receita / gasto if gasto > 0 else 0.0
        a["retorno"] = round(ret, 2)
        if orc <= 0:
            novo[a["id"]] = 0.0
            continue
        if vendas == 0 and gasto >= cfg["gasto_corte"]:
            props.append({"acao": "cortar", "anuncio": a["id"], "de": orc, "para": 0.0,
                          "motivo": f"gastou {gasto:g} sem nenhuma venda (limite {cfg['gasto_corte']:g})"})
            props.append({"acao": "trocar", "anuncio": a["id"],
                          "motivo": "subir um anúncio novo com outro gancho da reserva no lugar"})
            novo[a["id"]] = 0.0
        elif vendas >= 1 and ret >= cfg["retorno_min"] and medicao:
            novo[a["id"]] = orc * (1 + cfg["passo"])
            props.append({"acao": "subir", "anuncio": a["id"], "de": orc, "para": None,
                          "motivo": f"retorno {ret:.2f} ≥ {cfg['retorno_min']:g} com {vendas} venda(s)"})
        elif vendas >= 1 and ret < 1 and gasto >= cfg["gasto_corte"]:
            novo[a["id"]] = orc * 0.5
            props.append({"acao": "reduzir", "anuncio": a["id"], "de": orc, "para": round(orc * 0.5, 2),
                          "motivo": f"vende, mas devolve menos do que custa (retorno {ret:.2f})"})
        else:
            novo[a["id"]] = orc
            props.append({"acao": "manter", "anuncio": a["id"], "de": orc, "para": orc,
                          "motivo": "ainda aprendendo" if gasto < cfg["gasto_corte"] else f"retorno {ret:.2f}"})

    # regra 2: teto por dia. Se a soma passa, corta só o que sobe (proporcionalmente).
    # Cada subida usa só a folga que sobra até o teto; sem folga, fica onde está.
    if sum(novo.values()) > cfg["teto_dia"]:
        subindo = {p["anuncio"] for p in props if p["acao"] == "subir"}
        atual = {a["id"]: float(a.get("orcamento_dia", 0)) for a in ads}
        sem_subir = sum(atual[k] if k in subindo else v for k, v in novo.items())
        ganho = sum(novo[k] - atual[k] for k in subindo)
        folga = max(cfg["teto_dia"] - sem_subir, 0.0)
        f = min(1.0, folga / ganho) if ganho > 0 else 0.0
        for k in subindo:
            novo[k] = atual[k] + (novo[k] - atual[k]) * f
        alertas.append(f"Teto de {cfg['teto_dia']:g}/dia: as subidas foram ajustadas para caber.")
        if sem_subir > cfg["teto_dia"]:
            alertas.append(f"Mesmo sem subir nada, o total ({sem_subir:g}) passa do teto: corte algum anúncio.")
    for p in props:
        if p["acao"] == "subir":
            p["para"] = round(novo[p["anuncio"]], 2)
            if p["para"] <= p["de"]:
                p["acao"], p["motivo"] = "manter", p["motivo"] + " — sem espaço no teto do dia"
    total = round(sum(novo.values()), 2)
    return {"propostas": props, "alertas": alertas, "orcamento_total_proposto": total, "teto_dia": cfg["teto_dia"],
            "executa": False, "aviso": "PROPOSTA. Nada muda sem o OK do dono."}


def texto(r: dict) -> str:
    linhas = ["Clic · proposta de anúncios (nada muda sem o seu OK)", ""]
    for a in r["alertas"]:
        linhas.append(f"⚠ {a}")
    if r["alertas"]:
        linhas.append("")
    for p in r["propostas"]:
        if p["acao"] == "trocar":
            linhas.append(f"  ↻ {p['anuncio']}: {p['motivo']}")
        elif p["acao"] != "manter":
            linhas.append(f"  {p['acao'].upper():8} {p['anuncio']}: {p['de']:g} → {p['para']:g}/dia · {p['motivo']}")
    mant = [p["anuncio"] for p in r["propostas"] if p["acao"] == "manter"]
    if mant:
        linhas.append(f"  manter: {', '.join(mant)}")
    linhas += ["", f"Total proposto: {r['orcamento_total_proposto']:g}/dia (teto {r['teto_dia']:g}).",
               "Responda em uma linha: 'ok tudo', 'ok A1 A3' ou 'não'."]
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "--ajuda"):
        print(__doc__)
        sys.exit(0)
    r = propor(json.load(open(sys.argv[1], encoding="utf-8")))
    print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in sys.argv else texto(r))


if __name__ == "__main__":
    main()
