# Notas do kit (achadas ao fazer o reel da geladeira, 07/11/2026)

Não editei as ferramentas; contornei aqui no exemplo.

**Corrigido no kit em 07/11/2026:** 1 (`motor/terra.js` agora vem no kit), 2 (`montar.py` destaca a `chave` só na sua frase), 3 (legenda em cima no `reel.css`), 5 (storyboard lê `boceto.fonte`). O 6 virou pegadinha no `SKILL.md`.

1. **`motor/base.js` não carrega.** A linha 5 faz `import { TERRA } from './terra.js'`, e `motor/` não traz `terra.js`
   (veio do reel-ciencia-3d, onde ele existe). Qualquer página que importe `base.js` morre ao carregar.
   Contorno: `js/reel.js` copia só os ajudantes (`legenda`, `cartoes`, `quando`, `ligar`, `ramp/io/out3/win`), sem three.js.
   Correção sugerida: tirar o globo do `base.js` (ou mover para um `base3d.js`) e deixar um motor 2D para fotos.

2. **`chave` de cada frase não chega à legenda.** O `montar.py` só destaca o que está em `destaques` (lista global),
   então uma palavra marcada como chave numa frase fica amarela em TODA frase em que aparece ("calor" e "grade" acendem
   várias vezes). O método diz "uma chave por frase". Contorno: repeti as chaves em `destaques` e aceitei as repetições.
   Correção sugerida: `montar.py` ler `frases[].chave` e destacar só naquela frase.

3. **`reel.css` põe a legenda embaixo (`#leg top:1270px`)**, mas `metodo/imagem.md` pede legenda em cima.
   Contorno: sobrescrevi `#leg { top: 250px }` no `index.html`.

4. **`.fonte-linha` e `#conta small` com menos de 28 px** são acusados pelo `hyperframes check` (piso de leitura no celular).
   Subi para 28 px aqui; vale ajustar o `reel.css`.

5. **Storyboard: o esboço `cifra` mostra a palavra "fonte" genérica** e ignora `boceto.fonte` do roteiro. Pequeno.

6. **Fotos com `z-index` por cima do desenho:** ao trocar a ordem das fotos por `z-index` (para o dissolve), o SVG
   e os brilhos sumiram até ganharem `z-index` próprio. Não é bug do kit, mas vale como pegadinha no SKILL quando
   o kit ganhar o modo "fotos + desenho".

7. `gancho_check.py` passou de primeira (0 erro, 0 aviso); nenhum falso positivo encontrado.
