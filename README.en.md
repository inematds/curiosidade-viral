# curiosidade-viral

**Faceless AI curiosity reels, and the model that turns views into results.**

A voice explains while the screen shows an everyday object (the refrigerator, the onion, the phone) large and textured, with the invisible drawn over it. You provide the question; AI researches the facts with sources, writes 4 hooks, assembles the storyboard for your approval, and only then records the voice (locally) and renders the video (in code, without video AI).

And since going viral is the easy part, the kit includes the rest of the model: **two agents that only make recommendations** (Curio takes care of the account, Clic takes care of the ads with 4 rules written in code) and the **link tagged for each reel**, so you can see what brought each person in.

Complete guide: **https://inematds.github.io/curiosidade-viral/guia/** · Português: [README.md](README.md) · Español: [README.es.md](README.es.md)

## What’s included

| Folder | What it is |
|---|---|
| `SKILL.md` | the skill (Claude Code / Codex): the full step-by-step |
| `metodo/` | the rules: `gancho.md` (5 tests, formats, prohibited elements), `roteiro.md` (curiosity loop, duration, JSON format), `imagem.md` (the object always on screen, the invisible drawn, movement, sound) |
| `ferramentas/` | `novo.py`, `gancho_check.py` (checker), `storyboard.py`, `voz.py` (local voice aligned to the word), `montar.py`, `mezcla.py`, `preparar.py` |
| `motor/` | render base (HyperFrames + Three.js), local fonts |
| `agentes/` | `curio.md` + `curio_triagem.py`, `clic.md` + `clic_regras.py`, `link.py`, examples |
| `exemplos/geladeira/` | the demo reel, from script to MP4 |
| `docs/caso-e-metodo.md` | the real case (one week, an account from scratch) and what it teaches |
| `testes/` | `python3 -m unittest discover -s testes` |

## The process, from start to finish

🧠 = you (director) · 🤖 = AI (Claude Code / Codex, via subscription) · ⚙️ = script

| # | Step | Who | Command |
|---|---|---|---|
| 1 | The reel’s question and who watches | 🧠 | — |
| 2 | New folder | ⚙️ | `python3 ferramentas/novo.py <slug> "<pergunta>" --duracao 30` |
| 3 | Sourced facts (`fatos.md`) | 🤖 | — |
| 4 | 4 hooks + script + scenes + post copy | 🤖 | `exemplos/<slug>/roteiro.json`, `pie.txt` |
| 5 | Checker | ⚙️ | `python3 ferramentas/gancho_check.py exemplos/<slug>` |
| 6 | **Storyboard: the only approval checkpoint** | ⚙️ → 🧠 | `python3 ferramentas/storyboard.py exemplos/<slug> --abrir` |
| 7 | Local voice | ⚙️ | `python3 ferramentas/voz.py --projeto exemplos/<slug> exemplos/<slug>/roteiro.json` |
| 8 | Object images (3–5 views of the same thing) | 🤖 | Codex image_gen (subscription) or your own photos |
| 9 | Reel page | 🤖 | `index.html` + `js/` (copy the refrigerator example) |
| 10 | Clock + music + prepare | ⚙️ | `montar.py` → `mezcla.py` → `preparar.py` |
| 11 | Test + still frames | ⚙️ → 🧠 | `npx hyperframes check` · `npx hyperframes snapshot` |
| 12 | Render | ⚙️ | `npx hyperframes render --output renders/<slug>.mp4` |
| 13 | Review the MP4 | 🤖 + 🧠 | storyboard sheet + `checklists/antes-de-postar.md` |
| 14 | Tagged link | ⚙️ | `python3 agentes/link.py <url> --conta <conta> --onde reel --reel <slug>` |
| 15 | Post manually from your phone | 🧠 | — |
| 16 | Curio: sorts messages and suggests replies (4×/day) | ⚙️ → 🧠 | `python3 agentes/curio_triagem.py mensagens.json --link <link> --estado estado.json` |
| 17 | Clic: suggests pausing/scaling ads within the 4 rules | ⚙️ → 🧠 | `python3 agentes/clic_regras.py metricas.json` |

## Install

```bash
git clone https://github.com/inematds/curiosidade-viral.git
cd curiosidade-viral
bash instalar.sh
```

Requires Node.js 22+, ffmpeg, Python 3 with numpy. Local voice: Chatterbox + Whisper (your voice in `VC_VOZ=/caminho/voz.wav`).
Nothing here calls paid APIs.

## The 6 lessons from the case

1. Sell (or offer) what you already teach: the most common question was “how do you do that?”
2. Measure from the first minute: one day without tracking, 19 people opened the payment page and nobody bought.
3. Concentrate the budget: a few ads with budget returned about 2×; many with little budget returned about half.
4. Tag every link: a sale without a source can’t be repeated.
5. Automate customer service, not decisions: the agents make recommendations; you decide.
6. Organic content sells too: the bio generated sales without any ads.

The case numbers are from one week and are not a promise of results.

MIT License · INEMA · https://inema.club