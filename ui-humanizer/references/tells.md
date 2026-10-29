# Catálogo de tells de UI gerada por IA

Formato de cada entrada:
- **Como reconhecer:** o que se vê na tela.
- **No código:** assinatura que o `audit.py` ou um grep acha.
- **Por que a IA faz:** de onde vem o default.
- **Quem citou:** respostas da thread (ver `comentarios.md`). "Casos" = observado nos sites dissecados em `casos.md`, não citado diretamente.
- **Troca:** o que fazer no lugar.
- **Pode ficar quando:** a exceção legítima.

Classes:
- **A · assinatura de template.** Uma ocorrência já justifica mudança.
- **B · sistema por padrão.** Pesa quando 2+ aparecem juntos.
- **C · fraco sozinho.** Só aja se já houver A ou B na mesma página.

---

## A · Assinatura de template

### A1. Eyebrow acima do título (o "sub sub sub titulo")

- **Como reconhecer:** texto pequeno acima de cada `h1`/`h2`, sans serif, caixa alta, `letter-spacing` largo, cor de acento ou cinza. Muitas vezes com traço `—`, ponto `•` ou ícone ✨ antes. Tamanho bem menor que o título. Aparece em toda seção ("RECURSOS", "COMO FUNCIONA", "PLANO PRO", "ANTES").
- **No código:** `uppercase tracking-widest text-xs`, `.eyebrow`, `.kicker`, `.overline`, `.section-label`, `text-transform: uppercase` + `letter-spacing: .1em+`, `<p>` ou `<span>` logo antes de `<h2>`.
- **Por que a IA faz:** é o jeito mais barato de "dar hierarquia" e organizar seções sem pensar no conteúdo. Virou padrão de template de SaaS.
- **Quem citou:** @greco_dev ("porra de novo esse sub sub sub titulo"), @ivanchagasp (".eyebrow antes de headings"), @antonioducs ("aquela tag pequena em cima do título com ícone de brilho"), @BertuPeter71 ("sans serif, caixa alta, bastante tracking, geralmente com traço na frente e tamanho consideravelmente menor que o título"). Casos: Capelon, Detran-RO.
- **Troca:** corte. Se a informação é útil (categoria do artigo, data, número da seção num documento longo), coloque onde ela serve: breadcrumb, meta do post, dentro do próprio título, num índice lateral. O título da seção tem que se sustentar sozinho.
- **Pode ficar quando:** editorial/revista com categoria real (ex.: "Política" acima da manchete), documentação com numeração de seção, um único uso com função clara. Nunca em toda seção.

### A2. Palavra do título em gradiente

- **Como reconhecer:** uma ou duas palavras do headline com gradiente (roxo→rosa, azul→ciano, laranja→rosa).
- **No código:** `bg-clip-text text-transparent bg-gradient-to-r`, `background-clip: text`, `-webkit-background-clip: text`, `-webkit-text-fill-color: transparent`.
- **Por que a IA faz:** "dar destaque" ao benefício do headline com o efeito que mais aparece nos sites de startup dos dados de treino.
- **Quem citou:** @antonioducs ("a palavra do título em gradiente"), @ivanchagasp, @opaulojunqueira, @Lukekw_, @bakanoobzin, @El_Sinisttro (gradiente em geral).
- **Troca:** título numa cor. A ênfase vem do texto (uma palavra concreta, um número) ou de tamanho e peso. Se precisa de destaque visual, use a imagem.
- **Pode ficar quando:** a marca é literalmente um gradiente (ex.: identidade definida assim no guia da marca).

### A3. Headline bicolor (últimas palavras em outra cor)

- **Como reconhecer:** headline em cinza escuro com as últimas 1–3 palavras na cor de acento ("Chega de perder horas com **sua escala.**", "Sua escala organizada. **Sem complicação.**", "Por que escolher a **Capelon?**"). Primo do A2, sem gradiente.
- **No código:** `<h1>...<span class="text-primary|text-blue-600|text-accent">...</span></h1>`.
- **Por que a IA faz:** mesmo motivo do A2, versão "sóbria".
- **Quem citou:** casos (Capelon, em três seções). É a mesma família do que @antonioducs descreveu.
- **Troca:** título numa cor só. Se tem um termo-chave, ele já está no texto.
- **Pode ficar quando:** uma vez, num contexto editorial com motivo (ex.: o nome do produto em destaque no próprio logotipo do hero).

### A4. Display serif + últimas palavras em itálico

- **Como reconhecer:** headline em serif de display com as 1–2 últimas palavras em itálico. Frequentemente com fundo bege/creme, paleta marrom claro, verde-oliva ou pastel, e texto "calmo" ("A slower kind of morning", "Clareza para decidir melhor.").
- **No código:** `Playfair Display`, `Instrument Serif`, `DM Serif Display`, `Fraunces`, `Cormorant`, `Newsreader`, `EB Garamond` + `<em>`/`<i>`/`italic` dentro do `h1`. Fundos `#f5f0e8`, `#faf7f2`, `stone-50`, `amber-50`.
- **Por que a IA faz:** é o default "elegante/editorial" das skills de frontend que tentam fugir do visual SaaS. Virou o segundo template.
- **Quem citou:** @BertuPeter71 ("provavelmente é em Playfair Display e as duas últimas palavras são em itálico"), @Dan3pm ("qualquer coisa gerada pela skill /Frontend-design. Quase sempre uma fonte serifada com paleta marrom clara / pastel"). Casos: o site do @OF3TA ("Se Escute").
- **Troca:** se serif tem motivo (editorial, marca, setor), use sem o truque do itálico e com uma paleta que venha do conteúdo. Se não tem, a família do design system.
- **Pode ficar quando:** a marca usa essa fonte, ou é uma revista/livro onde itálico tem função (título de obra, termo estrangeiro).

### A5. Card com borda lateral (ou superior) pintada

- **Como reconhecer:** card ou callout com uma listra colorida de 3–4px na esquerda. Variante: listra no topo de cada card (Detran-RO), cores diferentes por card (Se Escute: verde, terracota, azul).
- **No código:** `border-left: 3px|4px solid`, `border-l-4`, `border-l-[3px]`, `border-t-4` em card, `border-inline-start`, `box-shadow: inset 4px 0 0`.
- **Por que a IA faz:** jeito barato de diferenciar cards e "categorizar" sem pensar em conteúdo.
- **Quem citou:** @limasmjoao ("aqueles card com borda lateral pintada"), @ivanchagasp ("border-left"), @El_Sinisttro ("cards com listra do lado"). Casos: Se Escute, Detran-RO (no topo).
- **Troca:** card sem listra. Se a categoria importa, escreva a categoria ou use agrupamento (seções, título de grupo). Se é aviso, use o componente de aviso do design system com ícone e texto.
- **Pode ficar quando:** status semântico real num app (erro/aviso/sucesso) e consistente com o design system.

### A6. Quotation block decorativo

- **Como reconhecer:** bloco de citação com aspas gigantes ou listra lateral, usado pra destacar uma frase de marketing que ninguém disse.
- **No código:** `<blockquote>` com borda lateral, `“` gigante posicionado absoluto, `.quote`, `.callout`.
- **Por que a IA faz:** "quebra o ritmo" da página sem precisar de conteúdo novo.
- **Quem citou:** @ivanchagasp ("quotation block").
- **Troca:** se é citação real (com pessoa, cargo, foto, fonte), tipografia de citação simples. Se é frase de marketing, ela vai pro texto ou sai.
- **Pode ficar quando:** citação verdadeira e atribuída.

### A7. Chip com bolinha pulsando

- **Como reconhecer:** badge "● Disponível agora", "● Live", "● Novo recurso", "● Aceitando clientes" com ponto verde que pisca. Variante: toast flutuante "● Escala publicada" sobre o mockup (Capelon).
- **No código:** `animate-ping`, `animate-pulse`, `@keyframes pulse|ping|blink`, `span.rounded-full.bg-green-500` dentro de pill.
- **Por que a IA faz:** simula "vida" e urgência sem dado real.
- **Quem citou:** @joaquimcassano ("Chip + ausência de imagens é oq mais entrega"), @vborotoo ("Chips (ainda mais aquelas bolinhas pulsando)"). Casos: Capelon.
- **Troca:** corte. Indicador de status só com status real e atualizado (sistema que pode cair, evento ao vivo, estoque).
- **Pode ficar quando:** status page, live stream, dashboard operacional.

### A8. Pill/badge com sparkle acima do hero

- **Como reconhecer:** pill pequena acima do headline: "✨ Novo: IA integrada", "🚀 Lançamento", "Powered by AI", com ícone de brilho e às vezes seta.
- **No código:** `rounded-full border px-3 py-1 text-xs` antes do `h1`, ícone `Sparkles` (lucide), `✨`.
- **Por que a IA faz:** é o eyebrow (A1) versão hero, herdado de landing pages de startup.
- **Quem citou:** @antonioducs ("aquela tag pequena em cima do título com ícone de brilho"), @wdoug_alves (pills).
- **Troca:** corte. Se há novidade real, ela merece frase própria ou link no topo (barra de anúncio) com informação concreta.
- **Pode ficar quando:** um anúncio real e datado, com link pra onde explica.

### A9. Emoji no lugar de ícone

- **Como reconhecer:** 🚀 ⚡ ✨ 🔒 📊 💡 🎯 como ícones de feature, bullets, títulos de card, botões. Na versão extrema ("categoria fubanga"), emoji pra todo lado.
- **No código:** caracteres de emoji em HTML/JSX fora de conteúdo do usuário.
- **Por que a IA faz:** é o "ícone" que não precisa importar nada.
- **Quem citou:** @kmoonxd ("Emojis entrega muito"), @opaulojunqueira ("emojis (não ícones, emojis mesmo)"), @El_Sinisttro ("emoji pra todo lado").
- **Troca:** um set de ícones coerente (um só, mesmo peso de traço) ou nenhum. Lista de features muitas vezes fica melhor só com texto bem escrito.
- **Pode ficar quando:** a marca é informal e o emoji faz parte da voz (e é pontual), ou é conteúdo do usuário (chat, comentário).

### A10. Roxo/índigo padrão do Tailwind

- **Como reconhecer:** acento violeta/índigo, botão roxo, gradiente roxo→rosa ou roxo→azul, glow roxo em fundo escuro.
- **No código:** `violet-500/600`, `indigo-500/600`, `purple-*`, `fuchsia-*`, `#8b5cf6`, `#7c3aed`, `#6366f1`, `#4f46e5`, `#a855f7`, `#9333ea`.
- **Por que a IA faz:** é a cor de exemplo da documentação e dos templates de Tailwind/shadcn, e virou "a cor de IA".
- **Quem citou:** @Cirilorde ("A cor roxa padrão do tailwind").
- **Troca:** cor de acento que venha da marca, do produto, da foto principal ou do setor. Uma só, usada pouco (botão principal, link, um destaque).
- **Pode ficar quando:** a marca é roxa. Aí use o roxo exato da marca, não o `violet-600`.

### A11. "Como funciona" em 3 passos com número no círculo

- **Como reconhecer:** três colunas, círculo com 1/2/3, título de uma palavra ("Configure. Monte. Revise."), duas linhas de texto. Variante: card "Antes" vs. "Com [produto]" (Capelon).
- **No código:** `rounded-full w-10 h-10 flex items-center justify-center` com número, `grid-cols-3`, `steps`, `how-it-works`.
- **Por que a IA faz:** é a seção padrão de landing de SaaS, cabe em qualquer produto.
- **Quem citou:** @antonioducs ("a seção de como funciona em 3 passos com número dentro de um círculo"). Casos: Capelon ("Configure / Monte / Revise", "Antes / Com Capelon").
- **Troca:** mostre o processo de verdade: print do produto em cada etapa, vídeo curto, exemplo real ("a Maria da padaria X montou a escala de 12 pessoas em 4 minutos", se o usuário tiver esse dado). Se o processo é óbvio, corte a seção.
- **Pode ficar quando:** o processo é realmente sequencial e não óbvio (onboarding, compra com etapas), e com conteúdo específico.

### A12. Glassmorphism

- **Como reconhecer:** cards e navbar translúcidos com blur, borda branca fina, sobre gradiente ou blob colorido.
- **No código:** `backdrop-filter: blur`, `backdrop-blur-*`, `bg-white/5|10|20`, `border-white/10|20`.
- **Por que a IA faz:** "parece moderno" e disfarça a falta de imagem com fundo colorido borrado.
- **Quem citou:** @Ricowtf_ ("Aqueles cards em glass morphism já não dá mais").
- **Troca:** superfície sólida. Blur só onde há conteúdo real atrás (navbar sobre foto ou vídeo).
- **Pode ficar quando:** interface de sistema que segue a linguagem da plataforma (ex.: app macOS/iOS com materials nativos).

### A13. Card que parece clicável e não faz nada

- **Como reconhecer:** card levanta, ganha sombra ou borda colorida no hover, cursor vira mãozinha, e não tem link nem ação. "Você espera uma ação e encontra só mais um bloco decorativo."
- **No código:** `hover:-translate-y-1`, `hover:scale-105`, `hover:shadow-xl`, `cursor-pointer`, `transition-all` em `div` sem `href`/`onClick`.
- **Por que a IA faz:** aplica hover em todo card pra "dar interatividade".
- **Quem citou:** @Fagner_Souza.
- **Troca:** hover só em elemento interativo. Card estático não reage. Se o card deveria levar a algum lugar, faça ele ser um link de verdade.
- **Pode ficar quando:** nunca sem ação.

---

## B · Sistema por padrão

### B1. Cara de SaaS pra qualquer negócio

- **Como reconhecer:** hero com headline abstrata + subtítulo + 2 CTAs + microcopy "sem cartão de crédito", logos "trusted by", grid de features, como funciona, depoimentos, pricing com 3 planos e o do meio "mais popular", FAQ, CTA final, footer de 4 colunas. Num site de padaria, escritório de advocacia, evento, igreja, órgão público.
- **Por que a IA faz:** é a estrutura de página mais frequente nos dados de treino.
- **Quem citou:** @eucaioba ("todos sites parecem de uma startup vendendo um SaaS, por mais que o site seja de uma padaria"), @OF3TA ("estética-saas-2026"), @aloneinthesukya. Casos: os três.
- **Troca:** estrutura do tipo de site real. Padaria: fotos, cardápio, horário, endereço, encomenda. Escritório: quem são, áreas, casos, contato. Evento: data, lugar, programação, ingresso. Órgão público: a lista de serviços, busca, o que precisa levar.

### B2. Grid de cards pasteurizados

- **Como reconhecer:** 3, 4 ou 6 cards iguais, cada um com ícone num quadradinho colorido + título + 2 linhas, mesmo tamanho, mesmo raio, mesma sombra. Variante "bento grid" com tamanhos aleatórios sem relação com importância.
- **No código:** `grid-cols-3` + `rounded-xl border p-6` repetido, ícone `lucide-react` em `div.rounded-lg.bg-primary/10`.
- **Quem citou:** @eucaioba ("componentes de card extremamente pasteurizado"), @vborotoo ("card padrão no-brainer"), @opaulojunqueira. Casos: os três.
- **Troca:** a forma vem do conteúdo. Itens com o mesmo peso → lista simples ou tabela. Um item mais importante → ele grande, os outros pequenos. Feature que se mostra → print dela. Texto corrido também é uma opção.

### B3. Ícone em quadradinho colorido (icon tile)

- **Como reconhecer:** ícone de linha dentro de um quadrado arredondado com fundo da cor de acento a 10%. Em todo card, toda lista, todo item de feature.
- **No código:** `rounded-lg|xl bg-*-50|100 p-2|3` envolvendo `<svg>`, `bg-primary/10`.
- **Quem citou:** casos (Capelon, Detran-RO). Faz parte do "card padrão" de @vborotoo.
- **Troca:** ícone solto, sem caixa, quando ajuda a escanear; sem ícone quando não ajuda.

### B4. Ausência de imagens

- **Como reconhecer:** a página inteira é texto, ícone, gradiente e cards. Nenhuma foto, print, gráfico ou pessoa.
- **Quem citou:** @joaquimcassano, @vborotoo. Casos: Se Escute, Detran-RO.
- **Troca:** material real. Ver fase 1 do SKILL.md. Placeholders explícitos se o material ainda não existe.

### B5. Pill e arredondado em tudo

- **Como reconhecer:** botões, badges, inputs, tags, abas, filtros, avatares, tudo `rounded-full`; todos os cards com raio grande; tudo "redondo/circular". Fileira de pills com setores ("Restaurantes, Bares, Clínicas...").
- **No código:** `rounded-full` em excesso, `rounded-2xl|3xl` em todo container, `border-radius: 9999px`.
- **Quem citou:** @wdoug_alves ("Shapes em forma de pill pra tudo quanto é lado"), @Lukekw_ ("botões arredondados"), @El_Sinisttro ("arredondamento pra todo lado"), @jeffpacheco_ ("muito redondo/circular"). Casos: Capelon (fileira de setores).
- **Troca:** escala de raio pequena (ex.: 0, 4, 8). Pill reservado a um tipo de elemento, se tanto. Cantos retos também são uma opção.

### B6. Gradiente de fundo / degradê colorido / neon

- **Como reconhecer:** blobs, mesh gradient, radial atrás do hero, seções alternando gradiente, glow neon em botão e borda, fundo escuro com padrão geométrico e divisor em onda (Detran-RO).
- **No código:** `bg-gradient-to-*`, `linear-gradient`, `radial-gradient`, `conic-gradient`, `blur-3xl` em div absoluto, `box-shadow: 0 0 40px <cor>`, `<svg>` de onda entre seções.
- **Quem citou:** @bakanoobzin ("uso exagerado de degradê colorido"), @opaulojunqueira, @ivanchagasp, @Lukekw_ ("Qualquer tipo de gradiente"), @El_Sinisttro ("Neon, Degradê").
- **Troca:** fundo sólido. A cor vem das fotos, da ilustração própria ou dos dados.
- **Pode ficar quando:** a marca usa, ou o gradiente representa algo (escala de dados, mapa de calor).

### B7. Animação genérica

- **Como reconhecer:** toda seção faz fade-up ao rolar, todo card faz `scale-105` ou sobe no hover, grids aparecem em stagger, números contam de 0 até o valor, marquee de logos infinito, hover idêntico em tudo.
- **No código:** `data-aos`, `framer-motion` com `whileInView`, `animate-fade-*`, `IntersectionObserver` + classe de entrada, `transition-all duration-300` em tudo.
- **Quem citou:** @slowrtz ("o estilo das animações da uma entregada firme"), @paaulo_133 ("As animações"), @Lukekw_ ("animação de hover sempre é a mesma").
- **Troca:** animação só onde explica algo: mudança de estado, feedback de clique, transição entre telas, revelar um dado. O resto entra parado. Respeite `prefers-reduced-motion`.

### B8. Biblioteca com tema de fábrica (shadcn, "standard claude library")

- **Como reconhecer:** componentes com o visual default intacto: cinzas zinc/slate, raio 0.5rem, `Card`/`Badge`/`Button`/`Tabs` de fábrica, sombra sutil igual, sidebar de app padrão. "A assinatura do Claude", reconhecível também em docs e slides.
- **Quem citou:** @metalheadlost ("Shadcn"), @accollctor ("o Claude principalmente parece que tem assinatura"), @gr33d1sg00d_ ("mais um com o standard claude library"), @iamgustavolima ("CLAUDE DESIGN"), @vborotoo ("Design system").
- **Troca:** aplicar os tokens do design system do projeto nos componentes (cor, raio, tipografia, espaçamento, densidade). Usar a biblioteca pela acessibilidade e comportamento, não pela aparência.

### B9. Layout padrão e divisão inorgânica das seções

- **Como reconhecer:** toda seção com o mesmo padding, mesma largura máxima, título centralizado + subtítulo centralizado + conteúdo, alternando fundo claro/cinza. Espaços vazios enormes sem motivo (Detran-RO). Ritmo idêntico do começo ao fim.
- **Quem citou:** @paaulo_133 ("divisão inorgânica das seções do site"), @vborotoo ("layout padrão"), @OnlyPedrinhu ("A organização do site"), @use_leadly ("formatação da página").
- **Troca:** ritmo vindo do conteúdo. Seções de tamanhos diferentes, alinhamento à esquerda como padrão, uma seção que quebra o grid quando merece (imagem sangrando, tabela larga), espaçamento que agrupa o que é relacionado.

### B10. Mockup de device flutuante + UI fake em volta

- **Como reconhecer:** print do produto dentro de um laptop/celular 3D inclinado, com sombra difusa, cercado de toasts e cards flutuantes ("● Escala publicada", "+32% este mês"), às vezes com dados claramente inventados.
- **Quem citou:** casos (Capelon).
- **Troca:** print real do produto, grande, reto, legível, com dados verossímeis do próprio usuário. Se quiser mostrar uma feature, recorte e amplie a parte que importa.
- **Pode ficar quando:** o mockup é a forma mais clara de mostrar que é um app mobile, sem os enfeites flutuantes.

### B11. Copy de template

Ver `copy.md`. Inclui headline abstrata, subtítulo que repete o headline, "Por que escolher a X?", "Mais X. Mais Y. Menos Z.", "Sem complicação", "Tudo em um só lugar", microcopy "Sem cartão de crédito · Cancele quando quiser", provas sociais genéricas, CTA "Consulte aqui" em caixa alta, excesso de texto.
- **Quem citou:** @OnlyPedrinhu ("as provas sociais a copy meio porca"), @ViUmaVaga ("Visual e palavras específicas"), @vborotoo ("excesso de texto").

---

## C · Fracos sozinhos

| ID | Tell | Quem citou | Quando agir |
|---|---|---|---|
| C1 | Fonte padrão (Inter, Geist, system, Plus Jakarta, DM Sans, Manrope) + "título minimalista" | @Lukekw_, @use_leadly | Junto com A/B. Uma sans boa pode ser a escolha certa. |
| C2 | Cada elemento de uma cor; várias fontes misturadas ("10 fontes") | @El_Sinisttro | Quando não há sistema por trás. |
| C3 | Sombras suaves e iguais em tudo | (extensão) | Junto com B2. |
| C4 | CTA de link em caixa alta com seta ("CONSULTE AQUI →", "SAIBA MAIS →") | casos (Detran-RO) | Junto com A1. |
| C5 | Carrossel com dots onde o ativo vira pill | casos (Detran-RO) | Se o carrossel esconde conteúdo importante. |
| C6 | Checklist com checks em círculo colorido | casos (Capelon) | Junto com B2/B11. |
| C7 | Microcopy de fricção zero sob o botão ("Sem cartão de crédito · 7 dias grátis · Cancelamento a qualquer momento") | casos (Capelon) | Junto com B1. |
| C8 | Dark mode azul-marinho quase preto com texto cinza claro como única opção | (extensão) | Junto com B6. |
| C9 | Botão de alternar tema na navbar de uma landing | casos (Capelon) | Se ninguém pediu. |

---

## Extensão · tells de fora da thread

A thread não citou estes, mas são a mesma escolha média aparecendo em detalhes, e aparecem muito em UI gerada depois que a pessoa já tirou o roxo e os cards. Marcados como extensão, no mesmo formato compacto. Classe pela regra de sempre (A age sozinho, B pesa em grupo, C só com A/B por perto).

| ID | Tell | Como reconhecer / no código | Troca | Pode ficar quando |
|---|---|---|---|---|
| E1 (A) | Faixa de atmosfera no hero | tira mono/caixa alta com substantivos abstratos ligados por ponto ou barra ("MARCA · MOVIMENTO · ESPAÇO", "TYPE / FORM / MOTION") na borda do hero | borda vazia, ou um fato concreto do produto ali | nunca como default |
| E2 (A) | "Role pra baixo" / scroll cue | "Scroll", "Role pra explorar", chevron ou mouse pulando; `animate-bounce` perto do fim do hero | corte: a página já rola, a próxima seção que convide pelo conteúdo | nunca |
| E3 (A) | Cursor piscando em texto estático | caret ou bloco piscando em headline ou terminal fake que ninguém edita; `@keyframes blink` em texto não editável | caret só onde dá pra digitar | campo de texto real, terminal real |
| E4 (A) | Pílula de versão/estado no hero | "BETA", "V0.6", "EARLY ACCESS", "INVITE-ONLY" no hero sem o brief ser de lançamento | status vai pra nav ou link de changelog; o hero vende o produto | anúncio real e datado de lançamento |
| E5 (A) | Faixa de hora/clima/local | chip tipo "Lisboa 14:23 · 18°C" ou relógio ao vivo que não é o produto | corte; hora e clima só se o produto é sobre lugar, viagem ou tempo | produto de lugar/viagem/tempo |
| E6 (B) | Fundo de grade ou bolinha decorativa | grade de linhas, papel milimetrado, pontos em `radial-gradient` esmaecendo na borda com `mask-image`, atrás de seção que não é canvas | superfície lisa, imagem real ou espaço | ferramenta que mede/alinha, com a grade nítida no workspace |
| E7 (B) | Número decorativo de seção | "01 — Descobrir", "02", "03" em seções que não são passos | numere só o que se lê/faz em ordem; senão o título basta | onboarding, processo com etapas reais |
| E8 (B) | Fileira de números grandes sem fonte | 3+ números enormes com legenda minúscula ("99%", "2.4M", "150+") logo abaixo do hero | um número só, real, com uma frase de contexto; senão corte | métrica real e atribuída |
| E9 (B) | Easing de mola/salto em UI de rotina | `animate-bounce`, `easeOutBack`/elastic, `cubic-bezier` com y < 0 ou > 1 em diálogo, menu, chip | ease-out curto que assenta uma vez | marca explicitamente lúdica, nunca em diálogo |
| E10 (B) | Virada de tema no meio da página | página clara que cai numa faixa escura (ou o contrário) no meio do scroll sem motivo de marca | escolha claro, escuro ou sistema uma vez; faixa contrária só pra um CTA/mídia real | uma única quebra para CTA ou mídia |
| E11 (C) | Duas bordas na mesma borda | borda de 1px **e** sombra larga definindo o mesmo card; ou `border-t` + `border-b` em toda linha de lista | escolha um tratamento de borda: fio **ou** elevação; um divisor só entre linhas | junto com B2/B9 |
| E12 (C) | Raio extremo em card pequeno | card pequeno com `rounded-3xl`/`rounded-[2rem+]` espremendo o conteúdo numa bolha | raio por papel: controle pequeno, card médio; raio grande é pra pill e mídia | junto com B5 |
| E13 (C) | Texto cinza sobre superfície colorida | `bg-*-600 text-gray-400`, cinza neutro sobre painel saturado | tinta clara, ou um tom da própria cor da superfície; confira o contraste | — |
| E14 (C) | Corpo justificado ou em caixa alta | `text-align: justify` ou `uppercase` em parágrafo | texto alinhado à esquerda, caixa de frase; caixa alta só em rótulo curto | rótulo curto, nunca parágrafo |

## Trocas que são o mesmo default (não faça)

| Saindo de | Não vá pra | Porque |
|---|---|---|
| Roxo do Tailwind | Bege + verde-oliva + serif | É o default do `/frontend-design` (A4) |
| Inter | Playfair com itálico | A4 |
| Gradiente | Glassmorphism | A12 |
| Emoji | Ícone lucide em quadradinho colorido | B3 |
| Eyebrow caixa alta | Eyebrow em serif itálico | Continua sendo A1 |
| Cards com sombra | Cards com borda lateral | A5 |
| Hero centralizado | Hero split texto/mockup flutuante | B10 |
| "Transforme seu negócio" | "Clareza para decidir melhor" | Continua abstrato (copy.md) |

A saída de verdade é sempre a mesma: voltar ao conteúdo, ao material real e às referências escolhidas pelo usuário.
