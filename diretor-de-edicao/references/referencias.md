Busca de referências. Um vídeo bom mostra a coisa real no instante em que ela é dita: o print da página com a frase marcada, o número na fonte, o logo da ferramenta citada, a foto do objeto. Ilustração genérica e card com texto repetindo a fala derrubam retenção. Por isso a busca vem antes do roteiro, e o roteiro já nasce sabendo o que vai aparecer em cada fala.


O navegador.

Você precisa navegar de verdade, não só buscar texto. Use, nesta ordem:

- Claude in Chrome (extensão), quando a página pede a sessão da pessoa (perfil do Instagram, LinkedIn, X, ferramentas que ela usa). Só leia e tire print; nunca curta, comente, siga, poste ou mude configuração.
- O navegador embutido do Claude Code ou Playwright, pra páginas públicas. Site que bloqueia navegador automatizado costuma passar com Chrome visível (`channel='chrome', headless=False`). Se aparecer CAPTCHA, pare e use outra fonte.

Diga em uma linha qual vai usar. Banner de cookies: recuse o não essencial.


O que buscar, por tipo.

| precisa de | onde buscar | como guardar |
|---|---|---|
| prova de um fato ou número | a fonte primária: documentação oficial, relatório, paper, blog de engenharia da empresa, órgão público, página do produto | print em 2× da página, com as caixas da frase exata pra marcar com marca-texto na palavra falada; URL e data em `refs/fontes.md` |
| a tela de um produto ou site | o próprio site, aberto no navegador | gravação de tela real (Playwright `record_video` ou a gravação nativa do sistema), tema claro, pop-ups fechados, sem dados pessoais |
| logo de ferramenta, marca, linguagem | Simple Icons (CC0), press kit oficial, Wikimedia Commons | SVG ou PNG transparente em `refs/logos/` |
| foto de objeto, lugar ou pessoa pública | Wikimedia Commons, Unsplash, Pexels, NASA, acervos públicos | arquivo + licença + autor em `refs/fontes.md`; CC BY exige crédito na legenda do post; nada NC ou ND |
| referência de estilo (cor, tipografia, composição, ritmo de edição) | Pinterest, Behance, Dribbble, Savee, Awwwards, e reels de criadores do nicho | 3–5 prints em `refs/estilo/` com uma linha cada dizendo o que copiar (paleta, peso de fonte, como o texto entra) e o que não copiar |
| como outros contam o mesmo tema | busca do Instagram, TikTok e YouTube Shorts pelo tema | ver abaixo |

Imagem do Pinterest ou de portfólio é referência, não asset: não entra no vídeo, a menos que a fonte original tenha licença pra isso.


Pedindo o vídeo de referência.

Peça à pessoa, em linguagem simples, numa mensagem só:

- O quê: 1 a 3 vídeos que ela gostaria que o dela parecesse. Pode ser de qualquer nicho; o que importa é a edição.
- Como mandar: o link do post (Reels, TikTok, Shorts, YouTube) ou o arquivo. Se o vídeo é privado ou não baixa, uma gravação de tela do celular com o som ligado serve.
- O que dizer sobre cada um: o que ela quer copiar. Dê exemplos pra ela marcar: o jeito que o texto aparece, a legenda, o ritmo dos cortes, os sons, as imagens que aparecem em cima da pessoa, o gancho, a duração, o enquadramento. E o que ela não quer.
- Qual escolher, se ela pedir ajuda: o mesmo formato que ela vai gravar (alguém falando pra câmera se ela vai falar pra câmera), duração parecida com a que ela quer, e de preferência um vídeo que foi bem acima do normal daquele criador (views bem maiores que a média do perfil), porque é ali que a edição está funcionando.

Quando chegar: baixe (`yt-dlp <link>`; se não baixar, peça a gravação de tela), transcreva, decomponha (`edicao.md`, "Replicar a edição de uma referência") e devolva em 3–5 linhas o que vai ser copiado e o que não dá pra copiar com o material dela (por exemplo, a referência usa vários cenários e ela gravou num só). Copia-se formato, ritmo e tipo de prova; nunca o conteúdo, a piada, a música ou as imagens da referência.

Se ela não tiver referência, procure você: 3 vídeos do mesmo formato e tema, escolhidos pelo critério acima, e mostre em uma tabela curta (link · views · o que pegar de cada um) antes do roteiro.


Reels de referência (pesquisa do tema).

1. Busque o tema nas plataformas (no Chrome da pessoa, se ela estiver logada) e anote 10–20 vídeos com views.
2. Compare dentro do mesmo criador: o vídeo dele que estourou contra um mediano. Isso tira o efeito do tamanho da conta.
3. Baixe os melhores com `yt-dlp` (só pra análise), transcreva com `scripts/transcribe.py` e monte a tabela: primeira fala e tempo, segunda fala e tempo, quando chega a primeira prova, o "segredo", o fim, o CTA.
4. Diga o que separa o que estourou do mediano. O padrão mais comum: o que estoura mostra primeiro o que todo mundo faz e a prova de que não funciona, e só então o truque; o mediano vai direto pros passos.

Copiar formato é normal. Copiar conteúdo, piada, cena, objeto ou música da referência não é. Trecho do vídeo de outra pessoa só entra com autorização da pessoa que pediu o vídeo e com crédito na tela e no post.


Prints bem feitos.

- Capture em 2× e recorte com margem pra frase caber inteira; print cortado no meio da frase é reprovado.
- Guarde as caixas de texto (Playwright `bounding_box` dos elementos) pra o marca-texto varrer exatamente a frase dita.
- Esconda pop-up, chat de suporte e banner antes de capturar.
- Borre e-mail, telefone, nome de pessoa comum e qualquer dado que ajude um ataque.
- Print ilegível no tamanho do celular vira re-tipografia do texto real, com a fonte citada.
- Prova que some (vaga, preço, contador) se captura no dia e se guarda.


O registro.

Tudo o que for usado entra em `refs/fontes.md`: arquivo · URL · data · o que prova · licença e autor. Número sem linha nesse arquivo não entra na fala. O registro também gera os créditos da legenda do post.
