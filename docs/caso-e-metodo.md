# Curiosidade viral — o caso e o método (07/11/2026)

Base: um experimento real de um criador (uma semana, outubro de 2026), analisado pelo INEMA.
Os números são dele, de uma semana, e não são promessa de renda.

## O que o caso mostra

1. **Formato repetível → skill.** Ele passou 3 a 5 reels de curiosidades ao Claude: "desmonta estrutura,
   ganchos, ritmo, cena a cena, e cria uma skill que faça tudo". Saíram reels sem rosto: uma voz explica
   e a tela mostra a coisa real (lava-louças, cebola, mel, juntas dos dedos).
2. **Resultado:** conta nova (18/10), 14 a 17 reels; o reel da lava-louças passou de 4,4 milhões de views, 0 → ~19 mil seguidores em uma semana.
3. **Ganho de alcance ao postar à mão:** quando o agente passou a postar sozinho, as views caíram; voltou ao manual.
   (É o que ele observou, sem teste controlado.)
4. **Monetização:** o produto é a própria skill (39 €, depois 59 €), com landing + Stripe + Meta Ads.
   Dois agentes de IA:
   - **Curio** (community manager): responde "como faz?" em DM e comentário e leva à página; cuida da bio;
     confere 4×/dia e só avisa se houver novidade; repassa queixas e reembolsos; lê as métricas.
   - **Clic** (anúncios): Pixel + API de conversões + Stripe (cada venda sabe de qual anúncio veio);
     120 $/dia em 4 campanhas; confere a cada 2 h; relatório seg/sex; corta anúncio sem venda e propõe outro;
     só sobe verba com ROAS ≥ 1,5, teto 150 $/dia; exclui quem já comprou.
   - **Regra de ouro:** "eles propõem, eu decido" (gastar, publicar, pausar).
5. **Números em 26/10:** 25 cobranças (1.209 € bruto), 505 $ em anúncios, ROAS ≈ 1,5 (17 vendas por anúncio),
   7 vendas orgânicas pela bio, 29,76 $ por venda. O que perdeu dinheiro: muitos anúncios com pouca verba (ROAS 0,53),
   EUA hispânico (0 vendas), um dia sem Pixel (19 checkouts, 0 compras).
6. **6 lições:** venda o que você já ensina · meça desde o 1º minuto · concentre a verba · etiquete cada link ·
   automatize o atendimento, não as decisões · o orgânico também vende.

## As regras do kit que valem a pena (o método, reescrito por nós)

- **Gancho com 5 testes:** o estranho vem primeiro · é algo do dia a dia de quem assiste ("seu", "você") ·
  deixa uma pergunta sem responder · dá pra entender de primeira, em voz alta · funciona sem som (quadro 0 mostra).
  Proibido: data/lugar na frente, "segundo um estudo", tom de notícia, "hoje vou te explicar", falar de si.
- **4 ganchos por reel, comparados de dois em dois** ("qual pararia mais gente que não te segue?"), sem dar nota;
  3 ficam de reserva para versões A/B.
- **Roteiro:** fala de amigo, entendível por criança de 10 anos, laço de curiosidade (cada frase responde a anterior
  e abre a próxima), uma coisa só, final que vira o gancho do avesso, ~2,7 palavras/s (30 s ≈ 80 palavras).
- **Imagem:** a coisa do gancho aparece grande em quase todas as cenas · primeiro como a pessoa conhece, depois por dentro ·
  o invisível desenhado por cima numa cor só · o errado em vermelho · fonte da cifra em cinza pequeno ·
  nada de ícone/emoji/slide · legenda em cima, nada embaixo dos botões da rede.
- **Fecho que se vê:** a câmera recua até o reel virar um celular e um dedo toca "Seguir" / "Enviar".
- **Uma única parada: o storyboard** (uma ficha por cena com quadro de amostra) antes de gastar voz e render.
- **"A IA não sabe prever viral"** (no teste deles acertou igual cara ou coroa) → comparar e olhar, não dar nota.

## O que já temos × o que falta

| Já temos | Falta (o que este caso traz de novo) |
|---|---|
| reel-ciencia-3d (3D "E se…?", fonte por número, voz local) | formato **curiosidade do dia a dia** (objeto de casa como protagonista) |
| video-codigo (vídeo em código, voz presa à palavra) | **portão do gancho** (5 testes + 4 ganchos comparados) e **storyboard** antes do render |
| r7ex / explicavideo / yt-pubx / metritds | **conta-experimento** medida do zero (seguidores, views, manual × automático) |
| atende-leads (WhatsApp → Telegram), grokbot-7-agentes | agentes **Curio** (atendimento da conta) e **Clic** (anúncios só propondo) com as regras acima |

## Proposta: projeto `curiosidade-viral` (nome provisório)

**Fase 1 — kit/skill (local, sem custo)**
- Skill nossa: idea → `fatos.md` (fonte por dado) → 4 ganchos → `gancho-check.py` (os 5 testes automatizáveis:
  começa com data/lugar/"segundo", tom de notícia, "eu/meu canal") → storyboard HTML → voz local do Nei → cenas
  (motor do reel-ciencia-3d) → revisão por quadros → entrega com legenda do post.
- PT de origem; guia PT/EN/ES em `guia/` (projetos-landing-guia); README com "O processo, do início ao fim".
- 3 demos de objeto de casa (ex.: geladeira, chuveiro, celular) → lives3 + metritds.

**Fase 2 — experimento de conta (decisão do Nei)**
- Uma conta nova (IG + TikTok) só de curiosidades, ou usar uma marca já existente no metritds.
- Planilha de medição diária: views, seguidores, salvamentos, envios; comparar post manual × agendado.

**Fase 3 — os dois agentes (kit `conta-viral-agentes`)**
- **Curio:** responde "como faz?" levando ao guia/inema.club, resumo 4×/dia no v3, repassa queixas.
- **Clic:** só lê métricas e **propõe** (cortar, subir, trocar), com as 4 regras escritas no código
  (sem OK não gasta, teto diário, só sobe com ROAS ≥ 1,5, corta rápido). Sem API de anúncios até o Nei autorizar.
- Funil INEMA: o conteúdo é grátis → o "produto" é a entrada no inema.club / Telegram (link etiquetado por reel,
  para saber qual vídeo trouxe a pessoa).

**Fase 4 — conteúdo sobre o caso**
- Explicavideo "Uma conta do zero a 4 milhões de views com IA — e o que dá dinheiro" (sem citar a fonte) + r7ex.
- Portal + tópico INEMA.VIDEOS.

## Travas
- Voz local, não ElevenLabs. Meta Ads / API do Instagram para responder DM = API não autorizada → só com OK explícito.
- Números do caso são dele, de uma semana, "não é promessa de renda": dizer isso se usar no vídeo.
