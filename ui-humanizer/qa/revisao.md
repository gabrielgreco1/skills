# Revisão renderizada: três telas, acessibilidade, severidade

O detector (`scripts/audit.py`) só acha o que tem assinatura no código. Metade dos tells só aparece na tela renderizada: layout padrão, cards todos iguais, falta de imagem, cara de SaaS, ritmo idêntico, mockup flutuante, e se o resultado bate com a intensidade declarada. Esta é a parte da fase 6 que precisa abrir a página.

Use o Chrome (skill `claude-in-chrome`) ou qualquer ferramenta de screenshot de navegador (Playwright, etc.). O que importa são as três telas e o formato do laudo, não a ferramenta.

## Capturar em três telas

| Tela | Tamanho |
|---|---|
| Desktop | 1440×900 |
| Tablet | 768×1024 |
| Mobile | 390×844 |

Tire do topo, do meio e do fim em cada uma. Em página longa, role e capture abaixo da dobra também (ou uma captura de página inteira). Pegue também a árvore de acessibilidade quando a ferramenta der (pra conferir foco e rótulos).

## O que marcar

- **Layout:** corte de conteúdo, rolagem horizontal, elemento fixo cobrindo conteúdo ou foco, grade quebrada no tablet.
- **Hierarquia:** sem primeira leitura clara (teste do borrão), dois botões principais brigando, título e CTA abaixo da dobra no mobile.
- **Tipo:** viúva (palavra sozinha na última linha) em título ou linha de apoio a 1440 e a 390; falta de `text-balance`/`text-pretty`.
- **Tell renderizado:** qualquer coisa do catálogo que o grep não vê — "tudo centralizado" sem motivo de intensidade, ritmo de seção idêntico, icon soup, imagem genérica, todos os cards com a mesma cara. Composição centralizada de propósito (Variação baixa) **não** é tell.
- **Intensidade:** o screenshot bate com os níveis declarados na frase de leitura? Se a leitura pedia Variação alta e saiu simétrico, isso é um achado, não gosto.

## Acessibilidade (nunca piore isto pra parecer menos IA)

A checagem rápida, de alto sinal. Boa parte dela segue as [diretrizes de interface web da Vercel](https://github.com/vercel-labs/web-interface-guidelines); vale buscar a lista completa delas quando o projeto for sério.

- Controle só de ícone tem `aria-label`.
- Foco visível: nada de `outline-none` sem um `focus-visible` no lugar.
- Formulário: `label`, `autocomplete`, colar permitido.
- `prefers-reduced-motion` respeitado; nenhum `transition: all`.
- Imagem tem `width`/`height`; imagem abaixo da dobra é `lazy`.
- Link de verdade (`a`/`Link`), não `div` clicável.
- Modo escuro define `color-scheme` e a cor dos controles nativos.
- Data e número formatados com `Intl.*`.
- Contraste AA: corpo ≥ 4.5:1, texto grande e UI ≥ 3:1.

Alguns destes o `audit.py` já pega (`outline-none`, `transition: all`, animação sem guarda).

## Laudo

Escreva como você falaria: direto, específico, sem "talvez a gente pudesse…". Nomeie a falha, depois o conserto. Termos de design em inglês; nome de fonte sempre marcado como fonte ("a fonte X").

```text
## Desktop 1440×900
- [alto] O botão secundário tem o mesmo peso do principal e está ganhando a briga. Vira link de texto.
## Mobile 390×844
- [crítico] O título tem 7 linhas e o CTA cai abaixo da dobra. Encurte a copy primeiro; só depois tire um degrau de tamanho.
```

Severidade: `crítico` (quebrado ou inutilizável) · `alto` (tell forte ou falha de hierarquia) · `médio` · `nit`.

Conserte crítico e alto, capture de novo e inclua os screenshots do depois. Não narre que "a QA não rodou" como se fosse etapa a cumprir: ou rodou e tem achado, ou não dava pra rodar e você diz por quê em uma linha.
