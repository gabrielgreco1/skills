#!/bin/bash
# Confere as ferramentas do diretor-de-edicao e mostra o que instalar.
ok(){ printf "  ok   %s\n" "$1"; }; no(){ printf "  falta %s  →  %s\n" "$1" "$2"; }
command -v ffmpeg >/dev/null && ok ffmpeg || no ffmpeg "brew install ffmpeg"
command -v yt-dlp >/dev/null && ok yt-dlp || no yt-dlp "brew install yt-dlp"
python3 -c "import numpy" 2>/dev/null && ok numpy || no numpy "pip3 install numpy"
python3 -c "import mlx_whisper" 2>/dev/null && ok mlx-whisper || no mlx-whisper "pip3 install mlx-whisper  (Apple Silicon; no Intel/Linux use faster-whisper e adapte transcribe.py)"
python3 -c "import playwright" 2>/dev/null && ok playwright || no playwright "pip3 install playwright && python3 -m playwright install chromium  (prints e gravação de tela)"
