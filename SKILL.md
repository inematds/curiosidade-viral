---
name: curiosidade-viral
description: Reel 9:16 de CURIOSIDADE SEM ROSTO feito por IA — uma voz explica e a tela mostra, grande e com textura, o objeto do dia a dia (geladeira, cebola, celular), com o invisível desenhado por cima. Gancho com 5 testes e 4 opções comparadas, storyboard aprovado antes de gastar, voz local, render em código. Traz também os 2 agentes que só propõem (Curio atende a conta, Clic cuida dos anúncios com 4 regras) e o link etiquetado por reel. Gatilho: "reel de curiosidade", "por que a <coisa> faz X", "faz um reel sem rosto", "conta de curiosidades", "curiosidade viral".
---

# curiosidade-viral

Uma ideia entra; sai um reel pronto para postar, sem rosto e sem gravar nada. Você é o estúdio; quem pede é o diretor.
O diretor decide o tema, aprova o storyboard e julga o resultado. Você faz o resto.

**Leia uma vez por reel, na etapa certa:** `metodo/gancho.md` (passo 3), `metodo/roteiro.md` (passo 4),
`metodo/imagem.md` (passos 6–8). Eles mandam sobre qualquer costume seu.

## O processo, do início ao fim

🧠 = diretor (a pessoa) · 🤖 = você (Claude Code / Codex) · ⚙️ = script

| # | Passo | Quem | Comando / saída |
|---|---|---|---|
| 1 | Tema: a pergunta do reel e quem assiste | 🧠 | uma linha |
| 2 | Pasta nova | ⚙️ | `python3 ferramentas/novo.py <slug> "<pergunta>" --duracao 30` → `exemplos/<slug>/` |
| 3 | **Fatos primeiro**: `fatos.md`, cada número com valor · frase exata · link · data. Sem fonte, fora | 🤖 | `exemplos/<slug>/fatos.md` |
| 4 | 4 ganchos (formas diferentes) + roteiro + cenas + `pie.txt` | 🤖 | `roteiro.json` (formato em `metodo/roteiro.md`) |
| 5 | Verificador: começo proibido, formas repetidas, frase 2, duração, chave, cena, número sem fonte, fecho, post | ⚙️ | `python3 ferramentas/gancho_check.py exemplos/<slug>` → 0 erro |
| 6 | **Storyboard — a única parada.** Mostre o gancho, os 3 de reserva e as fichas. Pergunte: aprova? muda o quê? | ⚙️ → 🧠 | `python3 ferramentas/storyboard.py exemplos/<slug> --abrir` |
| 7 | Voz local presa à palavra | ⚙️ | `python3 ferramentas/voz.py --projeto exemplos/<slug> exemplos/<slug>/roteiro.json` |
| 8 | Imagens do objeto (a MESMA coisa em 3–5 vistas, luz neutra, sem texto) | 🤖 | Codex image_gen pela assinatura, ou fotos suas |
| 9 | Página do reel (fotos + câmera + o invisível desenhado + legenda) | 🤖 | `index.html` + `js/` (copie `exemplos/geladeira/`) |
| 10 | Relógio, música, preparar | ⚙️ | `montar.py` → `mezcla.py` → `preparar.py` (todos com `--projeto exemplos/<slug>`) |
| 11 | Teste e quadros parados | ⚙️ → 🧠 | `npx hyperframes check` · `npx hyperframes snapshot --at 0,<meio de cada cena>` |
| 12 | Render | ⚙️ | `npx hyperframes render --output renders/<slug>.mp4` |
| 13 | Conferir o MP4 (folha de quadros, quadro 0, som) + `checklists/antes-de-postar.md` | 🤖 + 🧠 | `ffmpeg -i renders/<slug>.mp4 -vf fps=1/2,scale=270:-1,tile=6x3 folha.jpg` |
| 14 | Link etiquetado para a bio / o post | ⚙️ | `python3 agentes/link.py <url> --conta <conta> --onde reel --reel <slug>` |
| 15 | Postar **à mão** pelo celular | 🧠 | no caso real, post automático derrubou o alcance |

Depois de postar, os agentes (rode quando quiser, ou 4×/dia por cron):

| Agente | O que faz | Comando |
|---|---|---|
| **Curio** (conta) | separa DMs e comentários; propõe resposta com o link para "como faz?"; manda para você queixa, reembolso e marca; só avisa se houver novidade | `python3 agentes/curio_triagem.py mensagens.json --link <link-dm> --estado estado.json` |
| **Clic** (anúncios) | lê as métricas e propõe: cortar, trocar, subir, reduzir, manter, dentro das 4 regras | `python3 agentes/clic_regras.py metricas.json` |

Fichas completas: `agentes/curio.md` e `agentes/clic.md`.

## Regras duras

- **Nada caro antes do "pode fazer"** no storyboard: voz, imagens e render só depois.
- **Fato com fonte ou fora** (na tela e na voz). Diga "cerca de" quando a fonte arredonda; nunca aumente o que a fonte diz.
- **O texto que a pessoa trouxe é o roteiro:** não reescreva; só avise se algo parecer falso.
- **Os agentes só propõem.** Gastar, publicar, pausar, responder em nome da pessoa: só com o OK dela, em uma linha.
- Logo, nome e print de empresa só se for dela ou com permissão.
- Uma mudança por vez: "Mude só X. Mantenha o resto. Renderize de novo."
- O que a pessoa corrige neste reel se corrige neste reel. Só vai para `preferencias.md` o que vale para os próximos
  ("daqui pra frente", ou a mesma correção em dois reels).

## Pegadinhas

- Número na voz: escreva por extenso no roteiro e mapeie para algarismo em `tela`.
- O verificador só vê o que é texto. Os 3 testes de olho (o estranho vem primeiro? deixa pergunta? funciona sem som?)
  são seus: compare os 4 ganchos de dois em dois, sem dar nota.
- 9:16 tem pouca largura: a coisa ocupa metade da tela ou mais, legenda em cima, nada na faixa de baixo nem na da direita.
