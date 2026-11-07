# curiosidade-viral

[![Curiosidade viral](guia/assets/banner.jpg)](https://inematds.github.io/curiosidade-viral/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O curiosidade-viral é um kit (uma "skill" para o Claude Code ou o Codex) que faz reels verticais de curiosidade sem aparecer ninguém: uma voz explica e a tela mostra, de perto, um objeto do dia a dia. Serve para quem quer criar uma conta de conteúdo curto sem gravar e sem editar. O kit confere o gancho antes de gastar, pede a sua aprovação num storyboard, grava a voz no seu computador e monta o vídeo em código. Traz também dois agentes que leem mensagens e números de anúncios e só propõem. Precisa de Node.js, ffmpeg, Python e o Claude Code ou o Codex.

📖 Guia completo: **https://inematds.github.io/curiosidade-viral/guia/**

**Reels de curiosidade sem rosto feitos por IA, e o modelo que transforma views em resultado.**

Uma voz explica e a tela mostra, grande e com textura, a coisa do dia a dia (a geladeira, a cebola, o celular), com o
invisível desenhado por cima. Você dá a pergunta; a IA pesquisa os fatos com fonte, escreve 4 ganchos, monta o
storyboard para você aprovar e só então grava a voz (local) e renderiza o vídeo (em código, sem IA de vídeo).

E como viralizar é a parte fácil, o kit traz o resto do modelo: **dois agentes que só propõem** (Curio cuida da conta,
Clic cuida dos anúncios com 4 regras escritas em código) e o **link etiquetado por reel**, para saber o que trouxe cada pessoa.


## O que tem aqui

| Pasta | O que é |
|---|---|
| `SKILL.md` | a skill (Claude Code / Codex): o passo a passo inteiro |
| `metodo/` | as regras: `gancho.md` (5 testes, formas, proibidos), `roteiro.md` (laço de curiosidade, duração, formato do JSON), `imagem.md` (a coisa sempre na tela, o invisível desenhado, movimento, som) |
| `ferramentas/` | `novo.py`, `gancho_check.py` (verificador), `storyboard.py`, `voz.py` (voz local presa à palavra), `montar.py`, `mezcla.py`, `preparar.py` |
| `motor/` | base do render (HyperFrames + Three.js), fontes locais |
| `agentes/` | `curio.md` + `curio_triagem.py`, `clic.md` + `clic_regras.py`, `link.py`, exemplos |
| `exemplos/geladeira/` | o reel de demonstração, do roteiro ao MP4 |
| `docs/caso-e-metodo.md` | o caso real (uma semana, conta do zero) e o que ele ensina |
| `testes/` | `python3 -m unittest discover -s testes` |

## O processo, do início ao fim

🧠 = você (diretor) · 🤖 = a IA (Claude Code / Codex, pela assinatura) · ⚙️ = script

| # | Passo | Quem | Comando |
|---|---|---|---|
| 1 | A pergunta do reel e quem assiste | 🧠 | — |
| 2 | Pasta nova | ⚙️ | `python3 ferramentas/novo.py <slug> "<pergunta>" --duracao 30` |
| 3 | Fatos com fonte (`fatos.md`) | 🤖 | — |
| 4 | 4 ganchos + roteiro + cenas + texto do post | 🤖 | `exemplos/<slug>/roteiro.json`, `pie.txt` |
| 5 | Verificador | ⚙️ | `python3 ferramentas/gancho_check.py exemplos/<slug>` |
| 6 | **Storyboard: a única parada para aprovar** | ⚙️ → 🧠 | `python3 ferramentas/storyboard.py exemplos/<slug> --abrir` |
| 7 | Voz local | ⚙️ | `python3 ferramentas/voz.py --projeto exemplos/<slug> exemplos/<slug>/roteiro.json` |
| 8 | Imagens do objeto (3–5 vistas da mesma coisa) | 🤖 | Codex image_gen (assinatura) ou fotos suas |
| 9 | Página do reel | 🤖 | `index.html` + `js/` (copie o exemplo da geladeira) |
| 10 | Relógio + música + preparar | ⚙️ | `montar.py` → `mezcla.py` → `preparar.py` |
| 11 | Teste + quadros parados | ⚙️ → 🧠 | `npx hyperframes check` · `npx hyperframes snapshot` |
| 12 | Render | ⚙️ | `npx hyperframes render --output renders/<slug>.mp4` |
| 13 | Conferir o MP4 | 🤖 + 🧠 | folha de quadros + `checklists/antes-de-postar.md` |
| 14 | Link etiquetado | ⚙️ | `python3 agentes/link.py <url> --conta <conta> --onde reel --reel <slug>` |
| 15 | Postar à mão, pelo celular | 🧠 | — |
| 16 | Curio: separa mensagens e propõe respostas (4×/dia) | ⚙️ → 🧠 | `python3 agentes/curio_triagem.py mensagens.json --link <link> --estado estado.json` |
| 17 | Clic: propõe cortar/subir anúncios dentro das 4 regras | ⚙️ → 🧠 | `python3 agentes/clic_regras.py metricas.json` |

## Instalar

```bash
git clone https://github.com/inematds/curiosidade-viral.git
cd curiosidade-viral
bash instalar.sh
```

Precisa de Node.js 22+, ffmpeg, Python 3 com numpy. Voz local: Chatterbox + Whisper (sua voz em `VC_VOZ=/caminho/voz.wav`).
Nada aqui chama API paga.

## As 6 lições do caso

1. Venda (ou ofereça) o que você já ensina: a pergunta mais comum era "como você faz isso?".
2. Meça desde o primeiro minuto: um dia sem medir, 19 abriram o pagamento e ninguém comprou.
3. Concentre a verba: poucos anúncios com verba devolveram cerca de 2 vezes; muitos com pouca, cerca de metade.
4. Etiquete cada link: venda sem origem não se repete.
5. Automatize o atendimento, não as decisões: os agentes propõem, você decide.
6. O orgânico também vende: a bio vendeu sem anúncio nenhum.

Os números do caso são de uma semana e não são promessa de resultado.

Licença MIT · INEMA · https://inema.club
