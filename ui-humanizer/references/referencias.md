# Referências visuais: buscar, filtrar, extrair, decidir

Origem: @Hermes_sts ("vou no pinterest, baixo algumas imagens dahora e peço pro cursor criar arquivos de componentes com base nos designs que eu gosto. ao final, nem parece que foi IA"), @DavidMendonca01 ("dar referências de sites e seções que tu gostaria de seguir como inspiração"), @gr33d1sg00d_ (humano com gosto como supervisor).

Referência boa substitui a escolha média do modelo por escolhas de alguém. Por isso é a fase que mais tira a cara de IA, e também a mais fácil de estragar: muita referência hoje já foi gerada por IA.

## 1. Primeiro, pergunte ao usuário

Antes de buscar, peça:
- 2–5 sites que ele gosta (de qualquer setor) e o que gosta em cada um.
- Prints, fotos, boards do Pinterest, posts do Instagram, embalagens, a fachada da loja.
- Sites que ele **não** quer parecer.
- Concorrentes diretos (pra se diferenciar, não pra copiar).

O que o usuário traz vale mais que qualquer busca. Se ele trouxe, pule pro passo 4.

## 2. Buscar no navegador

Use o Chrome (skill `claude-in-chrome`). Abra uma aba nova, faça a busca, role a página e tire screenshots. Você analisa pelos screenshots; não precisa baixar nada. **Baixar arquivos exige permissão do usuário** (diga nome, origem e tamanho antes). Não faça login por ele nem aceite cookies não essenciais (recuse).

### Fontes, do mais útil pro menos

| Fonte | O que tem | Sem login? | Cuidado |
|---|---|---|---|
| Sites reais do mesmo setor e de setores vizinhos | O que funciona de verdade | Sim | Busque marcas pequenas e boas, não só as grandes |
| **Pinterest** (`pinterest.com/search/pins/?q=...`) | Volume enorme, moodboard, fotografia, embalagem, tipografia | Parcial: a grade carrega atrás do modal de login, dá pra ver por screenshot; links e descrições dos pins só logado | Tem filtro **"Menos IA"** nos chips do topo: use. Muitos pins de "website design" são mockups gerados por IA (bege, serif, "A slower kind of morning") |
| **Siteinspire** (`siteinspire.com/websites`) | Sites reais publicados, por categoria (Typographic, Minimal, Unusual Layout, E-Commerce) | Sim | Curadoria de agência/estúdio, pode puxar pro minimalismo |
| **Awwwards** (`awwwards.com/websites/`) | Sites premiados, filtro por categoria | Sim | Muito experimental; pegue a ideia, não o efeito |
| **Godly** (`godly.website`) | Sites com motion forte | Sim | Idem |
| **Land-book**, **Lapa Ninja**, **One Page Love** | Landing pages reais por setor | Sim | Muitas são SaaS; filtre pelo setor do usuário |
| **Dribbble** (`dribbble.com/search/<termo>`) | Conceitos visuais, ilustração, branding | Sim (feche o banner de cookies em "Reject All") | São **conceitos**, não sites publicados; muitos nunca funcionariam. Bom pra cor, tipografia, ilustração |
| **Behance** | Projetos completos de branding e web | Sim | Idem ao Dribbble |
| **Fonts In Use**, **Typewolf** | Tipografia aplicada em contexto real | Sim | Ótimo pra fugir de Inter/Playfair |
| **Mobbin**, **Savee**, **Cosmos** | Telas de app, moodboards | Exigem conta | Peça ao usuário se ele tem conta e quer logar ele mesmo |

### Como montar a busca

Combine **setor + qualidade + formato**, em inglês (mais resultados) e português:
- `bakery website`, `padaria site`, `artisan bakery branding`, `bakery menu design`
- Pelo que é específico do negócio: `sourdough packaging`, `neighborhood bakery photography`
- Por linguagem visual vinda do brief: `editorial website typography`, `brutalist website`, `swiss grid website`, `warm documentary photography website`
- Por seção: `restaurant menu web layout`, `pricing table editorial`, `event schedule website`
- Termos que puxam pra longe do template: `independent`, `studio`, `editorial`, `print-inspired`, `hand-drawn`, `documentary`

Evite termos que puxam o template: `modern`, `clean`, `sleek`, `SaaS`, `landing page template`, `UI kit`, `dashboard template`.

## 3. Filtrar (descartar referência com cara de IA)

Descarte qualquer referência que tenha 2+ tells A do `tells.md`. Sinais extras de imagem gerada por IA no Pinterest/Dribbble:
- Fotos de comida/produto perfeitas demais, luz igual em todas, textos ilegíveis ou sem sentido na imagem.
- Mockup com copy genérica em inglês ("Baking Smiles One Pastry At A Time") e marca inventada.
- Mesma paleta bege/marrom/serif em metade dos resultados.
- Nenhum link pra site real nem autor identificável.

Fique com 6–12.

## 4. Ficha por referência

Pra cada uma, escreva (curto):

```
Ref: <nome / url / "print do usuário 2">
Por que entrou: <o que ela faz que serve pra este projeto>
Layout: <grid, alinhamento, densidade, como as seções se dividem>
Tipografia: <famílias se identificáveis, contraste de tamanho, caixa, entrelinha>
Cor: <de onde vem a cor: foto, fundo, acento; quantas cores>
Imagem: <tipo de foto/ilustração, tamanho, como ocupa a página>
Detalhe memorável: <a coisa que só ela tem>
Não pegar: <o que nela é tell ou não serve>
```

## 5. Direções

Agrupe as fichas em **2–3 direções** com nome curto (ex.: "cardápio de papel", "documental de bairro", "tipográfico suíço"). Cada direção: 2–3 referências, 3 decisões concretas (tipo, cor, layout) e o que ela pede de material (ex.: "precisa de fotos da equipe").

Mostre ao usuário com os screenshots e deixe ele escolher, misturar ou descartar. Não escolha por ele em projeto público de marca.

## 6. Da referência ao design system

- Pegue a **lógica**, não a superfície: "a foto ocupa a largura toda e o texto fica pequeno embaixo" é uma decisão; "copiar o hero da marca X" é plágio.
- Misture 2–3 referências por direção, nunca uma só.
- Converta em tokens (fase 4 do SKILL.md): famílias, escala, cores com origem, raio, espaçamento, regras de imagem.
- Se o usuário quer componentes "baseados nos designs que gosto" (fluxo do @Hermes_sts), gere um componente por padrão observado, com nome descritivo (`MenuBoard`, `StoreHours`, `PhotoStrip`), e mostre lado a lado com a referência.

## 7. Da imagem ao código (quando há uma imagem pra seguir)

Quando o usuário trouxe um print/mockup, ou você gerou imagens de seção pra uma página nova inteira, não vá direto pro código "inspirado" nela. Extraia o sistema primeiro, depois construa pra bater.

Use este caminho quando: o usuário deu uma imagem de referência, **ou** você vai desenhar uma página nova/redesign completo e tem ferramenta de gerar imagem. Pule em edição pequena, componente isolado, ou trabalho dentro de um kit que já existe. Diga em uma linha qual caminho pegou.

1. **Tenha a referência.** Use a imagem do usuário, ou gere imagens em escala de seção (hero e seções-chave como imagens separadas, não um board comprimido). O hero tem que estar legível em tamanho de laptop pequeno; regenere se texto ou espaço estiver ilegível.
2. **Extraia o sistema e escreva antes de codar:** paleta (hex), famílias e escala de tipo, degraus de espaço, grade e divisão de colunas, regra de raio e borda, estilo de botão, e o que **evitar** — confira a própria referência contra o `tells.md`, porque imagem gerada também vem com tell.
3. **Implemente pra bater.** Siga a referência de perto; não "melhore" ela de volta pra um template. Mapeie os valores extraídos pros tokens do projeto (token do projeto vence quando conflita com a imagem).
4. **Compare** screenshot do que você fez contra a referência, na mesma tela; conserte o que ficou diferente.
5. **Grave** o sistema extraído no `DESIGN.md` do projeto se ele virar a cara oficial.

A intensidade é a mesma da leitura da página (ver `metodo/calibragem.md`): não há eixo separado pra imagem.

## 8. Registro

Salve as fichas e screenshots aprovados numa pasta do projeto (ex.: `design/referencias/`) se o usuário quiser, pra próxima sessão não recomeçar do zero.
