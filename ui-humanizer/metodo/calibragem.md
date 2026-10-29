# Calibragem: quanto empurrar, e pra onde

A regra principal da skill diz que toda escolha precisa de um motivo vindo deste produto. Falta uma coisa: **o quanto** empurrar. A mesma página pode estar certa calma e simétrica (um manifesto, uma bio) ou errada assim (uma landing de produto que precisa vender numa tela). Sem decidir a intensidade antes, a IA cai no meio-termo morno de sempre, que é justamente a escolha média que denuncia.

Então antes de qualquer pixel, decida duas coisas: **o que a pessoa vem fazer nesta página** (a intenção) e **três níveis de intensidade** que saem dessa intenção. Declare isso numa frase na fase 1 e a construção inteira passa a ter contra o que ser conferida.

## A frase de leitura (escreva na fase 1)

Uma linha, antes do código, que fixa a leitura da página:

> "Lendo isto como: `<página>` para `<público>`, uma página de `<intenção>` com linguagem `<visual>`, em `<stack>`. Intensidade: Variação `<baixa/média/alta>`, Movimento `<…>`, Densidade `<…>`."

Exemplo: *"Lendo isto como: página inicial de uma padaria de bairro para quem mora perto e quer encomendar, uma página de mostrar com linguagem documental e foto grande, em HTML/Tailwind. Intensidade: Variação alta, Movimento baixo, Densidade baixa."*

A frase não é burocracia: é o que deixa a auditoria objetiva. Se a página saiu simétrica e centralizada mas a leitura pedia Variação alta, isso é um erro verificável, não uma questão de gosto.

## Os três eixos

Cada eixo tem três níveis com **efeito observável** — dá pra olhar o resultado e dizer em qual nível ele está. Mexa num eixo de cada vez quando for ajustar, e diga qual e por quê.

### Variação — o quanto a composição se afasta da estrutura média

Variação é sobre **composição**, não sobre quantidade de elementos. Dá pra ter variação alta com pouquíssima coisa na tela: um título enorme jogado fora do eixo é variação alta com três elementos.

| Nível | O que se vê no resultado |
|---|---|
| Baixa | Simétrico, centralizado ou coluna única; ordem de seção convencional; todas as seções com a mesma largura. Aqui centralizar é escolha de propósito, não o "tudo centralizado" por preguiça. |
| Média | Base alinhada à esquerda com 1–2 quebras assimétricas (divisões 7/5, 8/4); uma seção que rompe a coluna (imagem sangrando, citação larga). |
| Alta | Assimetria na maioria das seções; elementos que se sobrepõem ou sangram; ordem de seção ou navegação fora do convencional. A variação vem da composição, não de deixar a fonte cada vez maior. |

Centralizar não é tell quando a leitura pede Variação baixa (frases curtas, convite, manifesto, uma coluna só). Vira tell quando é o default aplicado a tudo sem motivo. Esse é o critério pra separar o A1/B9 do catálogo de uma composição calma de propósito.

### Movimento — quanto se mexe, e quão perceptível

| Nível | O que se vê no resultado |
|---|---|
| Baixo | Só mudança de estado no hover e no foco; nenhuma entrada animada; ≤ 150ms. |
| Médio | Mais uma entrada por seção (fade/deslize ≤ 16px), em stagger de no máximo 3 itens; 200–300ms; tudo protegido por `prefers-reduced-motion`. |
| Alto | Mais movimento ligado ao scroll ou uma interação-assinatura só (ver `craft/padroes.md`); ainda só `opacity`/`transform`, ainda protegido. |

Movimento alto não quer dizer tudo se mexendo. Quer dizer **uma** coisa coreografada bem feita. Animação em toda seção vira o B7 do catálogo.

### Densidade — quanto conteúdo por tela

| Nível | O que se vê no resultado |
|---|---|
| Baixa | 1 ideia por tela; respiro grande entre seções; corpo 18px+; muito espaço vazio. |
| Média | 2–3 blocos por tela; corpo 16–17px. |
| Alta | Tabelas, listas de várias colunas, controles compactos; corpo 14–15px; números tabulares. |

Densidade não é bagunça. Densidade alta é uma tabela bem resolvida; bagunça é a mesma coisa sem hierarquia.

## Intenção da página → ponto de partida

Decida o que a pessoa vem **fazer nesta página**, não o que a empresa vende. A landing de uma ferramenta é "convencer"; a doc dela é "ler"; o painel logado é "operar". Cada intenção começa de um preset; ajuste dentro da faixa e declare na frase de leitura.

| Intenção | A pessoa está aqui pra… | Páginas típicas | Variação | Movimento | Densidade |
|---|---|---|---|---|---|
| Convencer | entender uma oferta e agir | landing, campanha, preços, cadastro | média–alta | média | baixa–média |
| Operar | fazer uma tarefa, repetidas vezes | painel, ajustes, editor, área logada | baixa | baixa | média–alta |
| Ler | aprender ou consultar | doc, central de ajuda, changelog, post | baixa | baixa | média |
| Mostrar | viver a obra em si | portfólio, galeria, case, lançamento | alta | média–alta | baixa |

O que a intenção muda além dos eixos:

- **Convencer:** a primeira tela diz a oferta e mostra a ação principal funcionando (um input ou botão de verdade, não um link pra ela). Prova tem que ser real.
- **Operar:** padrão conhecido ganha de novidade; o kit e os tokens do projeto ficam; a personalidade mora nos detalhes (estado vazio, microcopy, foco). Não reestilize um app que o usuário já aprendeu só pra "parecer menos IA" — isso quebra consistência e custa mais do que rende. Rode mesmo assim o detector e a checagem de acessibilidade, e aplique o resto só em telas novas ou quando pedirem redesign.
- **Ler:** medida de linha, hierarquia e navegação ganham da composição; sem hero de tela cheia; código e tabela ganham espaço.
- **Mostrar:** a obra lidera desde a primeira tela e a interface some; o movimento pode ser o ponto, sempre com alternativa pra quem reduz movimento.

Regras: se o usuário ou o briefing do projeto já fixam a intensidade, use a deles. Senão, nomeie a intenção, escolha um nível dentro da faixa e diga os dois na frase de leitura. Quando os eixos e uma regra do projeto brigarem, a regra do projeto vence (ver a ordem de fontes no `SKILL.md`).

## Como isso entra nas fases

- **Fase 0:** a intenção da página é a primeira coisa a nomear.
- **Fase 1:** a frase de leitura com os três níveis fecha o brief.
- **Fase 6:** a auditoria confere o resultado contra os níveis declarados — é um dos testes mais objetivos que a skill tem.
