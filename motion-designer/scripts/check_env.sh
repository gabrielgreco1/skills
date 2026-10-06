#!/bin/bash
# check_env.sh — verify (and offer to install) the motion pipeline toolchain.
miss=0
command -v ffmpeg >/dev/null || { echo "MISSING ffmpeg  -> brew install ffmpeg"; miss=1; }
python3 -c "import numpy" 2>/dev/null || { echo "MISSING numpy  -> pip3 install numpy"; miss=1; }
python3 -c "import PIL" 2>/dev/null || { echo "MISSING pillow -> pip3 install pillow"; miss=1; }
python3 -c "import playwright" 2>/dev/null || { echo "MISSING playwright -> pip3 install playwright && python3 -m playwright install chromium"; miss=1; }
command -v edge-tts >/dev/null || { echo "MISSING edge-tts (narration) -> pip3 install edge-tts"; miss=1; }
python3 - <<'PY' 2>/dev/null || { echo "MISSING chromium for playwright -> python3 -m playwright install chromium"; miss=1; }
from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()
PY
D=$(cd "$(dirname "$0")/.." && pwd)
[ -f "$D/lib/three/build/three.module.js" ] || { echo "MISSING lib/three (Three.js r170) — re-download the skill"; miss=1; }
# optional (recommended): Whisper transcript QC + background removal for photo cut-outs
python3 -c "import mlx_whisper" 2>/dev/null || echo "optional: pip3 install mlx-whisper   (qc_video.py transcript check, Apple Silicon)"
python3 -c "import rembg" 2>/dev/null || echo "optional: pip3 install rembg   (cut objects out of real photos)"
[ -f ~/.config/elevenlabs/api_key ] || [ -n "$ELEVENLABS_API_KEY" ] || echo "optional: ElevenLabs key not set (free edge-tts will be used unless the user provides one)"
command -v potrace >/dev/null || echo "optional: brew install potrace   (vectorize_logo.sh, crisp logos for beat edits)"
[ $miss = 0 ] && echo "toolchain OK" || exit 1
