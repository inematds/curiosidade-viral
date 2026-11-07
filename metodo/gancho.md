# O gancho: o primeiro segundo

Quem vê o reel não te segue e não pediu para ver. O gancho tem um segundo para fazer essa pessoa parar.
É a parte mais importante do vídeo e a que mais se reescreve.

## Os 5 testes (todos têm de passar)

| # | Teste | Pergunta para fazer | Exemplo que passa | Exemplo que reprova |
|---|---|---|---|---|
| 1 | **O estranho vem primeiro** | As 3 primeiras palavras já são a parte mais esquisita? | "Sua geladeira esquenta a cozinha." | "Em 1913, um engenheiro…" |
| 2 | **É algo da pessoa** | Fala de uma coisa que ela usa, vê ou sente, ou fala com ela ("você", "seu")? | "O seu celular…" | "Pesquisadores da Suíça…" |
| 3 | **Deixa uma pergunta** | Depois de ouvir, a pessoa quer saber o porquê? E o gancho NÃO responde? | "…e é por isso que ela funciona." | "…porque o gás tira o calor de dentro." |
| 4 | **Entende de primeira** | Dá para entender em voz alta, com palavras da rua, sem reler? | "A cebola tem uma arma." | "A cebola libera um composto sulfuroso volátil." |
| 5 | **Funciona sem som** | O quadro 0 mostra, grande e mexendo, a coisa do gancho, e o texto na tela a nomeia? | geladeira aberta soltando calor pela grade de trás | fundo preto com título |

## Formas que costumam parar

- Uma coisa do dia a dia que faz o **contrário** do que a pessoa acha.
- Um **objeto bobo** que faz algo enorme, com o objeto na frente.
- Um **número que não fecha**, com uma peça faltando.
- Algo **pessoal ou proibido** que poderia acontecer com ela.
- A pergunta sobre algo que **todo mundo já viu e ninguém perguntou**.

## Proibido no começo (o `gancho_check.py` acusa)

- Data, lugar ou "há X anos" na frente ("Em 1987…", "Na Noruega…").
- Ressalva na frente ("Segundo um estudo…", "Dizem que…", "Pelo visto…"). A ressalva vai na frase seguinte.
- Tom de notícia ("X acaba de lançar…", "X anunciou…") ou começar pela empresa.
- Anunciar em vez de intrigar: "Hoje eu vou te explicar", "No vídeo de hoje", "Presta atenção", "Olá", um título.
- Falar de quem faz o vídeo: "eu", "meu canal", "aqui no perfil".
- "Um dos maiores…", "Você sabia que…".
- Falar da plataforma ou da ferramenta (algoritmo, IA, app): quem assiste só quer saber o que acontece com ela.

## Logo depois do gancho

A frase 2 descarta a explicação que a pessoa já está pensando ("E não, não é por causa do gás.") ou diz a
pergunta em voz alta, se ela ainda não foi dita. Assim a pessoa não vai embora achando que já sabe.

## Como escolher

1. Escreva **4 ganchos**, cada um com uma forma diferente da lista acima, e cada um com a sua imagem do quadro 0.
2. Rode `python3 ferramentas/gancho_check.py <pasta>`: o que ele acusar, reescreva.
3. Compare de **dois em dois**: "com qual destes pararia mais gente que não me segue?". Sem dar nota.
   A IA não sabe prever o que viraliza; comparar funciona melhor do que pontuar. Na dúvida, o mais simples.
4. O vencedor vai para `gancho`; os outros 3 ficam em `reserva` (servem para uma versão B do mesmo reel).
