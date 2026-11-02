Voz gerada (só quando a pessoa não grava a fala toda).

Ordem de preferência: a voz da própria pessoa gravada na câmera; um clone da voz dela no ElevenLabs (IVC, a partir de 2–5 min de fala limpa); uma voz da biblioteca do ElevenLabs no idioma do vídeo; edge-tts (grátis, mais robótico). Peça a chave do ElevenLabs só se ela escolher, guarde em `~/.config/elevenlabs/api_key` com `chmod 600`, nunca no projeto, e avise que chave colada no chat deve ser trocada depois.

Receita que funcionou com clone em português: modelo `eleven_v4` (ou `eleven_v3`), stability 0,5, similarity 0,75, o roteiro inteiro numa requisição só. O v3/v4 lê ~25 % mais devagar que o multilingual_v2 (~3,4 palavras/s com pausas): planeje a duração com isso. Custa ~1 crédito por caractere; informe o gasto a cada chamada.

Uma tomada, intacta. Nunca re-espace pausas, cole frase de outra tomada ou acelere com `atempo`: a entonação quebra e a fala soa "bugada". Só apare cabeça e cauda. Mudou uma palavra do roteiro, gere o roteiro inteiro de novo. Por isso o texto é aprovado antes da voz.

Depois de cada tomada: transcreva e compare com o roteiro; ouça o primeiro 1,5 s sozinho (o modelo às vezes inventa uma sílaba antes da primeira palavra; apare até a primeira palavra real).

Siglas e termos estrangeiros: escreva como se fala no idioma do vídeo ("i-a", "a-pê-i", "S. Q. L.", "jêison"). Antes da tomada longa, teste cada termo novo na frase real em 2–3 grafias, junte num áudio numerado e deixe a pessoa escolher de ouvido. A leitura muda entre tomadas: depois de toda tomada nova, reouça as siglas no vídeo final. Termo que o modelo erra sempre e não é essencial sai da fala e fica só na tela. Na legenda, a grafia fonética volta pra palavra real.

Escrita pra voz: frases curtas, pausa só entre frases, nada de "..." nem vírgula no meio pra criar pausa, ênfase com CAIXA ALTA numa palavra, números por extenso.
