# Fundamentos: os números do "o que fazer no lugar"

O catálogo de tells diz o que não fazer. A fase 4 diz pra montar um design system mínimo. Este arquivo são os valores concretos pra isso, pra quando o projeto não tem tokens nem decisão própria. **Valor do projeto sempre vence** — isto é só o default pra não cair no default do modelo.

A ideia que amarra tudo: a escolha da IA é média porque é uniforme (um raio só, uma sombra só, uma fonte só, tudo do mesmo tamanho). A escolha de um designer é **desigual** — pesos, tamanhos, espaços e papéis variam de propósito. Os números abaixo existem pra criar essa desigualdade com sistema, não no olho.

## Tipografia

- Escolha a fonte de display primeiro, pela voz dela (vinda da leitura da página), e só depois uma fonte de texto que leia bem em 15–18px. Não comece pela fonte "segura".
- Pares que funcionam: grotesca de display + a mesma família no texto (contraste por peso e tamanho), bom pra ferramenta e produto dev; serif ou display de alto contraste + sans neutra no texto, bom pra editorial e leitura longa; mono só em dado, rótulo e código + sans no texto. Mono não é corpo de texto.
- Limite: no máximo 2 famílias (3 se uma for mono pra dado), 2–3 pesos cada. Dez fontes é tell; uma sans boa e bem usada não é.
- **Escala com razão**, não tamanhos soltos. 1.2 pra UI densa, 1.25–1.333 pra marketing. Em base 16px e razão 1.25: 13 · 16 · 20 · 25 · 31 · 39 · 49 · 61. Use `clamp()` nos dois degraus do topo.
- **Título principal:** pelo menos 2,5× o corpo no desktop (1,75× no mobile) e no máximo ~6rem. Tem que caber em 3 linhas a 1440px e 5 a 390px com a ação principal ainda visível sem rolar; se não couber, encurte o texto antes de diminuir a fonte. `line-height` 1.0–1.15; tracking levemente negativo (−0.01 a −0.03em) só nos tamanhos grandes, nunca mais apertado que −0.04em (glifos colando é tell).
- **Corpo:** 16–18px, `line-height` 1.5–1.7, medida de 60–75 caracteres por linha (`max-width: 65ch`). Linha mais larga que isso cansa.
- **Quebra:** título usa `text-wrap: balance`; corpo e linha de apoio usam `text-wrap: pretty`, pra uma palavra não ficar sozinha na última linha (viúva).
- **Números:** `font-variant-numeric: tabular-nums` em tabela, preço e estatística.
- Tracking largo só em rótulo curto, nunca no corpo. Peso fino (100–300) em tamanho grande fica frágil; display pede médio ou semibold, salvo quando a marca carrega aquela fonte fina de propósito.

## Espaço e ritmo

- **Uma escala só.** Base 4px: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128. Nada fora dela sem motivo.
- **Proximidade ganha de caixa.** O que é relacionado fica perto (8–16), grupos ficam separados (32–64), seções ficam longe (96–128 no desktop). Agrupar com espaço e alinhamento vem antes de desenhar um card (ver o B2 do catálogo).
- **Varie o ritmo por função da seção:** prova e fileira de logo densas, afirmação arejada, preço tabular. Não dê o mesmo padding e a mesma largura pra toda seção — ritmo idêntico do começo ao fim é o B9.
- No mobile, reduza o padding de seção (~0.6×) mantendo as proporções internas.

## Grade e layout

- 12 colunas no desktop, 4–6 no mobile; largura de conteúdo 1120–1280px, largura de texto 65ch.
- **Alinhamento acompanha a Variação** (ver `metodo/calibragem.md`). Variação baixa pode ser centralizada ou coluna única estrita — é composição válida, não tell. Variação média/alta puxa pra esquerda com divisões assimétricas; não force assimetria numa página que pediu calma simétrica.
- **Assimetria de propósito:** divisões 7/5 ou 8/4, um título que ocupa mais colunas que o texto dele, uma imagem sangrando por uma borda. Assimetria é a principal alavanca de Variação.
- Alinhe a poucas linhas verticais fortes. Todo elemento deveria dividir uma borda com algum outro.
- Full-bleed é pra imagem ou campo de cor, não pra texto. Centralize frase curta e CTA à vontade; mantenha leitura longa à esquerda, salvo quando a leitura escolheu a coluna central.

## Cor com função

- Comece do que a marca já tem (logo, produto, foto principal, tokens existentes). Só invente paleta quando não há nada. A cor vem do conteúdo, não do `violet-600` (ver A10/B6).
- **Estrutura:** 1 rampa neutra (8–10 degraus, levemente puxada pra cor da marca), 1 acento, mais as cores semânticas (sucesso, aviso, erro) usadas só pra estado.
- **Um acento, uma função.** O acento marca a ação principal e o estado atual. Se tudo é acentuado, nada é.
- Defina como variáveis CSS (`--cor-fundo`, `--cor-texto`, `--cor-suave`, `--cor-acento`, `--cor-borda`); nada de hex solto no componente.
- Contraste: texto de corpo ≥ 4.5:1, texto grande e UI ≥ 3:1. Confira principalmente o cinza suave. Texto cinza sobre superfície colorida costuma falhar — use tinta clara ou um tom da própria cor da superfície.
- Modo escuro é uma paleta própria (croma mais baixo, 2–3 degraus de superfície, `color-scheme: dark`), não uma inversão do claro. Canvas levemente fora do preto puro.

## Hierarquia

- Uma coisa principal por tela. Deixe o elemento mais importante claramente maior ou mais pesado; rebaixe o resto.
- No máximo 3 níveis de ênfase por seção (principal, secundário, suave).
- Um botão principal por tela; ação secundária é fantasma ou link de texto.
- Em linhas ou cards que se repetem, não carimbe o mesmo botão rotulado em cada item ("Abrir", "Ver mais"). Prefira um controle só com ícone e tooltip, um controle que aparece no hover da linha, ou uma ação no nível da seção, pra tela ficar leve. Mantenha `aria-label` quando o rótulo visível some.
- **Teste do borrão:** desfoque o screenshot (ou aperte os olhos). Você ainda deveria ver o que ler primeiro e onde clicar. Se tudo tem o mesmo peso, a hierarquia falhou.

## Movimento

- Movimento explica mudança (entrada, saída, estado). Não é decoração.
- 150–300ms pra UI, até 500ms pra entradas grandes; ease-out na entrada, ease-in na saída.
- Anime só `opacity` e `transform`. Proteja tudo que não é essencial com `prefers-reduced-motion`. Nunca `transition: all`.
- Nada de bounce, elástico ou overshoot em UI de rotina (diálogo, menu). Mola só onde a marca é explicitamente lúdica.

## Imagem

- Prefira o produto de verdade: print de UI, visualização de dado real, foto real da coisa. Mostre o print num tamanho legível e recorte a parte que importa.
- Decoração abstrata (blob, mesh, forma 3D) só quando faz parte da marca documentada.
- Nenhuma imagem é melhor que imagem genérica. Sem material, mande um hero só de tipografia e peça mídia real; não preencha o buraco com atmosfera (ver B4).
