# Briefing de design do projeto (um arquivo por projeto)

A fase 4 monta um design system mínimo. O problema: ele vive na cabeça daquela sessão e some. Na sessão seguinte a IA redescobre tudo do zero e volta pro default. A solução é gravar as decisões num arquivo do próprio projeto, que vira a fonte de verdade das próximas sessões.

Chame de `DESIGN.md` na raiz do repositório (ou `docs/DESIGN.md` se o projeto guarda docs lá). Um por app que tem marca própria; num monorepo, um por app, e os pacotes compartilhados apontam pro dele.

**Quando criar:** numa página nova, num redesign ou numa mudança de tokens. Não crie pra um conserto de uma linha.

Ele descreve **este** projeto. Default que vale pra qualquer projeto mora nesta skill, não no arquivo do projeto.

## Ordem de leitura (quem está acima vence no conflito)

1. Tokens e design system que já existem no código (tema, variáveis CSS, config do Tailwind, kit de componente).
2. O `DESIGN.md` do projeto.
3. Os defaults desta skill.

Quando o código e o `DESIGN.md` discordam, o código é a verdade do que está no ar hoje: conserte o `DESIGN.md` ou abra um `TODO`, não reestilize calado. E lembre: **default não é fonte de verdade** — token que bate com um tell do catálogo (roxo de fábrica, Inter em tudo, um raio e uma sombra só) não se herda só por estar no arquivo de tema. Fica só o que é genuinamente da marca: logo, UI do produto, foto real, paleta documentada.

## Bloco de tokens legível por máquina

Mantenha no topo das seções de visual um bloco que o `audit.py` (e qualquer grep) consegue ler, pra apontar fonte, hex e raio que aparecem no código mas não estão na lista:

```design-tokens
fonts: <família de display>, <família de texto>, <família mono>
colors: <#…>, <#…>, <#…>, <#…>, <#…>
radii: 0, <6px>, <10px>, 9999px
```

Valor em hex ou variável CSS, nunca só o adjetivo ("cinza quente" → `--cor-suave: #8A857D`). Toda regra com um *porquê* em uma linha. Um acento por superfície, com a função escrita.

## Esqueleto

```markdown
# DESIGN.md — <projeto>

## 1. Verdade do produto
- Quem usa, em que situação, em que aparelho.
- O que o produto faz por essa pessoa, em uma frase.
- Restrições: marca que fica, acessibilidade, idiomas, orçamento de performance, legal.
- Sucesso é: o resultado observável por página ("na landing, a pessoa encomenda; no painel, acha o turno vago em < 10s").
- Material real disponível: prints, dados, citações, logos que a IA pode usar, com caminho.

## 2. Leitura e intenção das páginas
Lendo isto como: <página> para <público>, linguagem <visual>, em <stack>.
| Página | Intenção (convencer/operar/ler/mostrar) | Variação | Movimento | Densidade |
|---|---|---|---|---|
| <Landing> | convencer | <alta> | <média> | <baixa> |
| <App>     | operar    | <baixa> | <baixa> | <alta>  |

## 3. Direção visual e proibições do projeto
- Direção: 3–5 frases concretas.
- Proibições além do catálogo da skill.
- Exceções permitidas ao catálogo, com motivo ("a marca é literalmente roxa, hex X").

## 4. Cor (com o bloco design-tokens acima) + a função de cada token
## 5. Tipografia (display, texto, mono, escala, corpo)
## 6. Espaço e grade (escala, colunas, padding por função de seção)
## 7. Componentes (raio por papel, elevação, botões, kit — que fica em app logado)
## 8. Movimento (durações, easing, o que anima, comportamento com movimento reduzido)
## 9. Imagem e conteúdo (de onde vêm foto, dado, citação; voz da copy)
## 10. Faça / Não faça
## 11. Registro de decisões (abaixo)
## 12. Referências (boards, marca, Figma, site no ar)
```

## Registro de decisões

Lista só de acréscimo com as decisões **fortes**, pra a IA reusar em vez de redescobrir. Fica na seção 11 do `DESIGN.md`, ou num `DESIGN-DECISOES.md` irmão se passar de ~20 entradas.

Registre quando travar um token, uma proibição, uma regra de composição, uma mudança de intensidade de uma página, ou uma mudança na ordem de fontes. Não registre conserto de rotina.

```markdown
### AAAA-MM-DD — <título curto>
- Contexto: …
- Decisão: …
- Porquê: …
- Não faça: …
- Páginas: marketing | app | ambas
- Refs: PR / URL / screenshot
```

## Quando atualizar

Depois de uma decisão durável, atualize a seção relevante **e** acrescente uma entrada no registro. É o que faz a próxima sessão começar de onde esta parou, em vez de voltar pro default.
