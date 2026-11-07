# O roteiro: fazer a pessoa ficar até o fim

O Instagram e o TikTok mostram o reel para mais gente quando ele é visto **inteiro** e quando é **enviado** a alguém.
O roteiro existe para isso.

## Antes de escrever, 4 linhas

1. **Quem assiste** e o que essa pessoa usa ou já viu que o tema toca.
2. **O puxão**: o que torna o tema quase inacreditável para essa pessoa. Um só.
3. **A pergunta** que o gancho deixa. Só é respondida inteira no fim.
4. **A prova**: os fatos do `fatos.md` que respondem, cada um com número ou coisa com nome e a fonte.

## As regras

- **Fala de amigo.** Frases com cola ("então", "por isso", "só que"), nada de frase de livro.
- **Uma criança de 10 anos entende** de primeira, sem voltar o vídeo.
- **Laço de curiosidade:** cada frase responde o que a anterior deixou e abre a próxima pergunta.
- **Uma coisa só:** o vídeo inteiro conta o que o gancho abriu.
- **Nenhuma frase sobra:** se tirar e nada se perde, tire.
- **O concreto ganha:** coisa com nome, número que dá para sentir, cena que a pessoa já viveu.
- **O fim vira o gancho do avesso:** a última frase antes do fecho responde a pergunta e mostra a coisa de sempre de outro jeito.
- **Fato com fonte ou fora.** Cada número no `fatos.md` com link e a frase exata, conferido no dia.
- **Escreva o fim logo depois do gancho.** O meio é o caminho de um até o outro.

## Duração

Cerca de **2,7 palavras por segundo**: 15 s ≈ 40 palavras, 30 s ≈ 80, 45 s ≈ 120, 60 s ≈ 160.
Curiosidade: ~30 s. Produto ou serviço: 20–35 s. Não estique para caber no tempo.

## Fecho

O fecho é sempre o mesmo da conta (fica em `preferencias.md`). No INEMA:
"Manda para quem sempre te pergunta isso." ou "Tem mais no inema.club."

## roteiro.json

O mesmo formato do reel-ciencia-3d (blocos e frases, que o `voz.py` e o `montar.py` leem), com quatro campos a mais:

```json
{
  "id": "geladeira",
  "voz": "nei",
  "duracao": 30,
  "publico": "adulto que tem geladeira em casa",
  "pergunta": "por que a geladeira esquenta a cozinha?",
  "gancho":  {"texto": "Sua geladeira esquenta a sua cozinha.", "forma": "contrario",
              "imagem": "geladeira de perto, grade de trás vermelha soltando ondas de calor"},
  "reserva": [
    {"texto": "…", "forma": "numero", "imagem": "…"},
    {"texto": "…", "forma": "objeto", "imagem": "…"},
    {"texto": "…", "forma": "pergunta", "imagem": "…"}
  ],
  "fecho": "Manda para quem deixa a porta aberta.",
  "blocos": [
    {"id": "b0", "cena": "gancho", "frases": [{"id": "g", "texto": "Sua geladeira esquenta a sua cozinha.", "chave": "esquenta"}]},
    {"id": "b1", "cena": "porta", "frases": [{"id": "f1", "texto": "E não, não é por causa da luz.", "chave": "luz"}]}
  ],
  "cenas": {
    "gancho": {"entrada": "corte", "que": "geladeira cheia na tela, grade de trás acende vermelha",
               "boceto": {"tipo": "objeto", "texto": "ESQUENTA"}, "som": ""},
    "porta":  {"entrada": "corte", "que": "…", "boceto": {"tipo": "cifra", "texto": "35 °C", "detalhe": "atrás da geladeira"}}
  }
}
```

- `blocos[0]` é o gancho escolhido (a mesma frase de `gancho.texto`).
- `chave`: a palavra da frase que vai destacada. Uma por frase, no máximo. Lidas em sequência, as chaves contam o vídeo.
- `cenas.<nome>.boceto.tipo`: `objeto`, `cifra`, `comparar` ("Antes|Depois"), `lista` ("Um|Dois|Três"), `dentro`
  (a coisa por dentro), `celular` (o fecho no celular). O storyboard desenha cada um.
- `pie.txt` (ao lado): o texto do post. Primeira linha engancha; sem hashtag; sem travessão longo.
