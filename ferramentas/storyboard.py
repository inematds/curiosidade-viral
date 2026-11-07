#!/usr/bin/env python3
"""Gera <pasta>/storyboard.html: uma ficha por cena, antes de gastar voz e render.

Uso:  python3 ferramentas/storyboard.py <pasta-do-reel> [--abrir]

Cada ficha mostra um esboço da composição (do campo boceto), as frases com a chave destacada, quanto tempo
dura (2,7 palavras/s), como entra e o que soa. No topo: o gancho escolhido e os 3 de reserva.
É o único ponto de parada do processo: o diretor aprova, muda ou pede outra versão aqui.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

PPS = 2.7


def esc(s):
    return html.escape(str(s or ""))


def marca(texto, chave):
    t = esc(texto)
    if chave:
        t = re.sub(re.escape(esc(chave)), lambda m: f"<mark>{m.group(0)}</mark>", t, count=1, flags=re.I)
    return t


def esboco(b):
    tipo = (b or {}).get("tipo", "objeto")
    tx, det = esc(b.get("texto")), esc(b.get("detalhe"))
    if tipo == "cifra":
        return f'<div class="sk cifra"><b>{tx}</b><small>{det}</small><i>fonte</i></div>'
    if tipo == "comparar":
        a, _, c = (b.get("texto") or "A|B").partition("|")
        return f'<div class="sk comparar"><div>{esc(a)}</div><div class="vs">×</div><div class="red">{esc(c)}</div></div>'
    if tipo == "lista":
        itens = "".join(f"<li>{esc(x)}</li>" for x in (b.get("texto") or "").split("|"))
        return f'<div class="sk lista"><ol>{itens}</ol></div>'
    if tipo == "dentro":
        return f'<div class="sk dentro"><div class="obj"></div><div class="lupa">{tx}</div></div>'
    if tipo == "celular":
        return f'<div class="sk celular"><div class="tel"><div class="obj mini"></div><span>{tx or "Seguir"}</span></div></div>'
    return f'<div class="sk objeto"><div class="obj"></div><b>{tx}</b></div>'


CSS = """
:root{--bg:#0c0c10;--card:#16161d;--tx:#ecebe6;--mut:#9a98a3;--am:#FACC15;--red:#ff4d3d;--inv:#38bdf8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.5 Inter,system-ui,sans-serif;padding:24px 16px}
h1{font-family:Sora,Inter,sans-serif;font-size:26px;margin:0 0 4px}h2{font-size:15px;color:var(--mut);font-weight:500;margin:0 0 20px}
.top{max-width:1100px;margin:0 auto 24px}.gancho{background:var(--card);border:1px solid #2a2a35;border-radius:14px;padding:16px 18px;margin-bottom:10px}
.gancho b{color:var(--am)}.res{color:var(--mut);font-size:14px;margin:4px 0}.res em{color:var(--tx);font-style:normal}
.warn{background:#3a1d1a;border:1px solid var(--red);border-radius:10px;padding:10px 14px;margin:8px 0;font-size:14px}
.grid{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{background:var(--card);border:1px solid #2a2a35;border-radius:14px;overflow:hidden}
.q{aspect-ratio:9/16;background:radial-gradient(circle at 50% 42%,#2b2b36 0,#0c0c10 70%);position:relative;display:flex;align-items:center;justify-content:center}
.meta{padding:12px 14px;font-size:14px}.meta .n{font-family:Sora,sans-serif;font-weight:700}.meta .d{float:right;color:var(--am)}
.meta p{margin:6px 0}.meta .que{color:var(--mut)}mark{background:var(--am);color:#0c0c10;padding:0 3px;border-radius:3px}
.tag{display:inline-block;border:1px solid #3a3a46;border-radius:99px;padding:0 8px;font-size:12px;color:var(--mut);margin-right:4px}
.sk{width:84%;text-align:center}.obj{width:62%;aspect-ratio:1;margin:0 auto 10px;border-radius:22px;background:linear-gradient(145deg,#d7d7dc,#6e6e78);box-shadow:0 0 60px #ffffff22}
.obj.mini{width:40%}.sk b{font-family:Sora,sans-serif;font-size:26px;color:var(--am);display:block}
.cifra b{font-size:46px}.cifra small{display:block;color:var(--tx)}.cifra i{display:block;color:var(--mut);font-size:11px;margin-top:6px}
.comparar{display:flex;gap:8px;align-items:center}.comparar div{flex:1;background:#24242e;border-radius:10px;padding:18px 6px;font-weight:700}
.comparar .vs{flex:0;background:none;color:var(--mut)}.comparar .red{color:var(--red)}
.lista ol{text-align:left;margin:0;padding-left:22px;font-weight:700}.lista li{margin:8px 0}
.dentro .lupa{position:absolute;right:12%;top:30%;width:44%;aspect-ratio:1;border:3px solid var(--inv);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--inv);font-weight:700;background:#0c0c10cc}
.celular .tel{width:58%;aspect-ratio:9/18;margin:auto;border:3px solid #55555f;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.celular span{background:var(--am);color:#0c0c10;border-radius:8px;padding:2px 10px;font-weight:700;margin-top:8px}
.leg{position:absolute;top:9%;left:8%;right:8%;font-family:Sora,sans-serif;font-weight:700;font-size:15px;text-align:center}
.zona{position:absolute;bottom:0;left:0;right:0;height:16%;background:repeating-linear-gradient(45deg,#ffffff08 0 6px,transparent 6px 12px)}
.zona.d{top:30%;bottom:16%;left:auto;width:13%;height:auto}
footer{max-width:1100px;margin:24px auto 0;color:var(--mut);font-size:14px}
"""


def gerar(pasta: Path):
    r = json.loads((pasta / "roteiro.json").read_text(encoding="utf-8"))
    cenas = r.get("cenas") or {}
    ordem, por_cena = [], {}
    for b in r.get("blocos", []):
        c = b.get("cena", "?")
        if c not in por_cena:
            ordem.append(c)
            por_cena[c] = []
        por_cena[c] += b.get("frases", [])
    avisos = []
    total = 0.0
    cards = []
    for i, c in enumerate(ordem):
        info = cenas.get(c, {})
        fr = por_cena[c]
        seg = sum(len(f.get("texto", "").split()) for f in fr) / PPS
        total += seg
        if not info.get("boceto"):
            avisos.append(f"cena {c} sem boceto")
        frases = "".join(f"<p>{marca(f.get('texto'), f.get('chave'))}</p>" for f in fr)
        leg = esc(" ".join(fr[0].get("texto", "").split()[:4])) if fr else ""
        som = f'<span class="tag">som: {esc(info["som"])}</span>' if info.get("som") else ""
        cards.append(f"""<div class="card"><div class="q">{esboco(info.get('boceto'))}<div class="leg">{leg}…</div>
<div class="zona"></div><div class="zona d"></div></div><div class="meta"><span class="n">{i+1}. {esc(c)}</span>
<span class="d">{seg:.1f} s</span>{frases}<p class="que">{esc(info.get('que'))}</p>
<span class="tag">entra: {esc(info.get('entrada','corte'))}</span>{som}</div></div>""")
    alvo = r.get("duracao")
    if alvo and abs(total - alvo) > alvo * 0.25:
        avisos.append(f"duração estimada {total:.0f} s × pedida {alvo} s")
    g = r.get("gancho") or {}
    res = "".join(f'<p class="res">reserva ({esc(x.get("forma"))}): <em>{esc(x.get("texto"))}</em> — {esc(x.get("imagem"))}</p>'
                  for x in r.get("reserva", []))
    warn = "".join(f'<div class="warn">⚠ {esc(a)}</div>' for a in avisos)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard {esc(r.get('id'))}</title><style>{CSS}</style></head><body>
<div class="top"><h1>Storyboard · {esc(r.get('id'))}</h1><h2>{len(ordem)} cenas · ≈ {total:.0f} s · pergunta: {esc(r.get('pergunta'))}</h2>
<div class="gancho">gancho ({esc(g.get('forma'))}): <b>{esc(g.get('texto'))}</b><br><small>quadro 0: {esc(g.get('imagem'))}</small></div>
{res}{warn}</div><div class="grid">{''.join(cards)}</div>
<footer>Faixa listrada = botões da rede (nada importante ali). Aprova, muda uma cena ou troca o gancho por um da reserva.
Voz e render só começam depois do "pode fazer".</footer></body></html>"""
    out = pasta / "storyboard.html"
    out.write_text(doc, encoding="utf-8")
    return out, avisos


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a or "--ajuda" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0 if a else 2)
    out, avisos = gerar(Path(a[0]))
    for x in avisos:
        print("AVISO", x)
    print(out)
    if "--abrir" in sys.argv:
        subprocess.Popen(["xdg-open", str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
