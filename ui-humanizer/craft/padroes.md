# Padrões que valem a pena

O catálogo de tells é metade da história: o que não mandar. Esta é a outra metade: movimentos que valem buscar quando a leitura da página pede Movimento ou Variação mais altos (ver `metodo/calibragem.md`). Sem isto, a fuga do template vira só "tirar coisa", e a página fica correta e sem graça.

Duas regras antes de qualquer um deles:

1. **Uma assinatura por página, mais 2–4 apoios quietos.** Dois movimentos fortes brigando pela mesma tela é ruído. Escolha o que é a cara desta página e deixe o resto discreto.
2. **Todo padrão tem um ponto em que vira tell.** Cada entrada abaixo tem a linha "vira tell quando". Confira antes de mandar, e sempre com alternativa pra quem reduz movimento. Anime só `opacity` e `transform`.

Nenhum destes é obrigatório. São ferramentas pra quando a intenção é convencer ou mostrar com Movimento médio pra cima; numa página de operar ou ler, quase nenhum entra.

## Entrada em ordem de leitura

Na entrada do hero, os pedaços chegam na ordem em que se lê (nav, título, apoio, ação principal, depois o secundário), cada um com uma subida curta e fade, pra conduzir o olho em vez de estourar tudo de uma vez. `opacity 0→1` mais `translateY` de até 16px, 300–500ms cada, irmãos 80–120ms apart, tudo pronto em ~1,2s pra ação já ser usável cedo. Espere `document.fonts.ready` pra linha não refluir no meio. **Vira tell quando:** vira entrada de página inteira (aí é o B7) ou quando há um rótulo acima do título na sequência (A1). O estado final tem que ser visível sem JS.

## Revelação única ao entrar na tela

Blocos abaixo da dobra sobem e fazem fade uma vez quando entram na viewport; um grupo pequeno cai em cascata. `opacity` + `translateY` de até 16px, 200–300ms, no máximo 3 itens em stagger; dispare com IntersectionObserver e `once: true`. **Vira tell quando:** anima todo parágrafo, rodapé e linha de lista — aí a leitura passa a esperar o movimento. Fade + escala + deslize no mesmo card é exagero; escolha um.

## Linha de display subindo de uma fenda

Linhas (ou palavras) de um título de display sobem de dentro de um recorte `overflow: hidden`, então o tipo parece **colocado** em vez de surgido no fade. Cada linha num wrapper com overflow escondido; o span interno vai de `translateY(110%)` a 0, 400–500ms ease-out, linhas 100–140ms apart. Dê o texto inteiro como `aria-label` no pai e esconda os spans da leitura assistiva. **Vira tell quando:** empilha com cascata de caractere, scramble ou máquina de escrever; ou quando o tipo passa do teto do hero (≤ ~6rem).

## Afirmação revelada no ritmo do scroll

Uma frase curta em tipo grande vai de uma tinta apagada pra tinta cheia, palavra por palavra, conforme a pessoa rola por ela, pra o ritmo de leitura casar com o de scroll. Só `opacity`, estado inicial ainda legível (texto grande a 3:1 ou mais). Um bloco por página, nunca em corpo de texto. **Vira tell quando:** mais de um bloco na página, ou usado em texto que precisa ser lido inteiro, ou com estado inicial abaixo de 3:1.

## Cards empilhados grudando

De 3 a 5 itens de uma sequência real (cases, etapas de processo) grudam um depois do outro; cada novo desliza sobre o anterior, que encolhe de leve com a borda de cima ainda à mostra. Cada item num slot `sticky` próprio, só `transform`. **Vira tell quando:** mais de cinco itens, ou itens que não são uma sequência de verdade.

## Profundidade pelo cursor num hero em camadas

As camadas de uma imagem realmente separada deslizam quantidades diferentes com o ponteiro, e um hero parado ganha profundidade. É a interação-assinatura única da página. Normalize o ponteiro pra −0.5…0.5 e interpole a cada frame; camadas de fundo contra o ponteiro, as da frente a favor, poucos pixels. Só em `(hover: hover) and (pointer: fine)` e sem preferência de movimento reduzido; toque recebe a composição parada. **Vira tell quando:** parallax numa foto de banco chapada, ou num mascote/objeto 3D genérico (ver abaixo, mídia genérica).

## Tipo fixo sobre um corte de vídeo

A imagem em movimento troca (um corte, um crossfade entre clipes) e a tipografia fica ancorada: o tipo é a constante, a mídia é a variável. Desligue o `loop` nativo e faça fade no fim do clipe voltando da cor da página, trocando com crossfade de `opacity` de ≤ 500ms. O fundo da página é igual à cor de borda da imagem. **Vira tell quando:** cortes sem motivo, ou a imagem é material de IA genérico.

## Composição de hero ancorada

Ponha a copy do hero num lugar deliberado pra a mídia ficar limpa: canto inferior esquerdo editorial, dividida em cima e embaixo feito capa de revista, ou rótulos nos quatro cantos ao redor da imagem. Texto nunca sobre o rosto/assunto; reposicione a mídia (`object-position`) antes de encolher o tipo. `100dvh` com fallback `100vh`. **Vira tell quando:** os cantos viram estatística inventada (A-de-prova-falsa), faixa de palavras de atmosfera, hora/clima local ou um "role pra baixo".

## Assunto rompendo o quadro

Profundidade por camada: a imagem do hero fica num quadro embutido e um recorte real do assunto (o produto, a pessoa) passa por cima da borda do quadro ou do título. O recorte é irmão acima do quadro, ancorado embaixo. **Vira tell quando:** o recorte é mascote, personagem NFT ou objeto de cromo flutuando no vazio; ou é uma borda rasgada feita por `clip-path` em vez de um recorte preparado.

## Borda da mídia igual à página

O fundo da página é a cor pra qual o vídeo ou a foto cai nas bordas, então o hero não precisa de overlay, não tem emenda e não pisca. A primeira regra de CSS põe esse fundo no `html, body`; proteja o texto com a ferramenta mais leve que funciona (um canto calmo da imagem, uma sombra de texto suave, um fade tardio só na borda de baixo). **Vira tell quando:** vira um scrim quase opaco que enterra a imagem (ver B4/imagem).

## Sistema de rótulo de metadado

Um estilo quieto de rótulo pra metadado real (datas, locais de trabalho real, créditos) que faz valer um único momento grande de display. 11–13px, curto, caixa alta ou versalete com tracking largo (é onde tracking largo mora), em mono ou na fonte de texto, contraste ≥ 4.5:1. Nunca acima de um título. **Vira tell quando:** vira rótulo acima do título (A1), numeração decorativa de seção, ou faixa de atmosfera.

## Botão com rótulo que rola

No hover, o rótulo do botão rola pra cima e uma cópia nova entra por baixo; uma seta ao lado gira. O rótulo nomeia a ação. Cópia duplicada escondida da leitura assistiva; movimento reduzido vira só mudança de cor. **Vira tell quando:** rola em todo link da página.

## O que foi descartado de propósito

Ideias que parecem "premium" mas caem direto num tell do catálogo — não use como default:

- Fade com blur (`filter: blur`) na entrada: anime só opacity/transform. A subida sem blur já resolve.
- Palavra em serif itálico no meio de um título sans: é o A4.
- Vidro líquido, superfície fosca, blur progressivo de fundo: A12.
- Texto com gradiente, varredura de brilho, ring de gradiente animado, borda cônica girando: A2/B6 e loop infinito de atenção.
- Mola e overshoot (menu cápsula, check saltitante): movimento de rotina não salta.
- Máquina de escrever com cursor piscando, scramble/decode: movimento explica mudança; troca de caractere não é opacity/transform.
- Contador de 0 até o número, fileira de estatística no canto: número só se for real e com uma frase de contexto.
- Cluster de avatares "junte-se a +10k" acima do título, badge de anúncio, chip de eyebrow: A1/A8 e prova falsa.
- Marquee infinito, relógio/clima ao vivo, bolinha "disponível" pulsando: loop de atenção (A7) e faixa de atmosfera.
- Mídia de IA genérica no hero (anéis de neon em estátua, cromo surreal, mascote, mandala girando, objeto flutuando em vazio de vidro): a técnica em volta pode servir, a imagem é que entrega. Mostre a coisa real.
