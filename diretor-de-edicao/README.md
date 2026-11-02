# diretor-de-edicao — uma skill de Claude Code pra editar vídeo curto

Edita os takes que você gravou e entrega o vídeo pronto pra Reels, TikTok, Shorts, YouTube ou LinkedIn:
- corta por palavra, com jump cut;
- monta o formato "yap", você falando pra câmera com textos, prints, logos e imagens aparecendo em cima;
- monta o formato tela + rosto;
- põe legenda palavra por palavra e sons virais nos momentos certos.

Antes de editar, busca na internet, pelo navegador, as referências, prints e imagens que provam o que você fala. Também escreve o roteiro e diz o que gravar quando você ainda não gravou.

## Instalar
1. Copie esta pasta pra `~/.claude/skills/diretor-de-edicao/`.
2. Ferramentas (macOS, Apple Silicon recomendado):
   ```bash
   brew install ffmpeg yt-dlp
   pip3 install numpy mlx-whisper playwright && python3 -m playwright install chromium
   ```
   Depois rode `bash scripts/check_env.sh`.
3. Pra busca de referências em sites onde você está logado, instale o Claude in Chrome. Sem ele, a skill usa o navegador embutido ou o Playwright.
4. No Claude Code: "edita esse vídeo" com os takes anexados, "me ajuda a fazer um roteiro de Reels sobre …", ou `/diretor-de-edicao`.

A primeira pergunta é o idioma. Depois vêm:
- o que você tem: vídeo gravado, só o gancho, só a ideia, um vídeo pra revisar ou uma referência pra copiar o estilo;
- o formato;
- a plataforma;
- duração, CTA, legenda e sons;
- quem narra: você na câmera, voz de IA, ou os dois;
- 1 a 3 vídeos de referência, dizendo o que você gosta em cada um. Se você não tiver, a skill procura.

## O que tem dentro
| caminho | o quê |
|---|---|
| `SKILL.md` | o fluxo: perguntas, referências, roteiro, produção, QC e entrega |
| `references/referencias.md` | como buscar prova, prints, logos, fotos, referência de estilo (Pinterest e outros) e reels de referência, e registrar a fonte de cada um |
| `references/roteiro.md` | pesquisa antes de escrever, autorrevisão, estruturas por tipo de vídeo, regras de escrita (sem frase de efeito, explicação antes do exemplo), gancho, CTA, ideias |
| `references/retencao.md` | o que segura gente nos primeiros 25 s, com os números de um estudo com centenas de Reels |
| `references/edicao.md` | corte do A-roll, os 3 primeiros segundos, yap, tela + rosto, legenda, áreas seguras, CTA na tela, sons virais, replicar uma referência, render |
| `references/narracao.md` | voz gerada (ElevenLabs/edge-tts), quando a fala não é gravada |
| `references/gravacao.md` | o que mandar pra pessoa antes de ela gravar |
| `references/entrega.md` | checklist e entrega (arquivo, versão leve, legenda do post) |
| `scripts/transcribe.py` | transcrição com tempo por palavra (mlx-whisper) e o início da voz |
| `scripts/cut_aroll.py` | monta o A-roll a partir de uma lista de trechos por palavra: bordas pela energia da voz, silêncios encurtados, jump cut com punch-in |
| `scripts/qc_static.py` | acha trechos de tela parada |

Combina com a skill [`motion-designer`](../motion-designer), que é chamada quando uma cena pede animação.

## Licença dos sons
Sons de meme e músicas quase nunca têm licença livre. Em post orgânico é prática comum. Se o vídeo virar anúncio ou for monetizado, troque por versões CC0 (Pixabay, Freesound) ou use a biblioteca de áudio da própria plataforma.
