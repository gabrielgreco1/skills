#!/bin/bash
# check_env.sh — verify (and offer to install) the motion pipeline toolchain.
# Detects the platform package manager and the working pip entry point, so the hints are copy-pasteable
# everywhere (macOS, Arch, Debian/Ubuntu, Fedora, openSUSE).
miss=0
if command -v brew >/dev/null; then PM="brew install"
elif command -v pacman >/dev/null; then PM="sudo pacman -S"
elif command -v apt-get >/dev/null; then PM="sudo apt-get install"
elif command -v dnf >/dev/null; then PM="sudo dnf install"
elif command -v zypper >/dev/null; then PM="sudo zypper install"
else PM=""; fi
if command -v pip3 >/dev/null; then PIP="pip3 install"
elif python3 -m pip --version >/dev/null 2>&1; then PIP="python3 -m pip install"
else PIP=""; fi
sys() { if [ -n "$PM" ]; then echo "$PM $1"; else echo "your package manager's $1"; fi; }
py()  { if [ -n "$PIP" ]; then echo "$PIP $1"; else echo "pip install $1 (or your distro's python-*-package)"; fi; }
need() { echo "MISSING $1 -> $2"; miss=1; }

command -v ffmpeg >/dev/null || need ffmpeg "$(sys ffmpeg)"
python3 -c "import numpy" 2>/dev/null || need numpy "$(py numpy)"
python3 -c "import PIL" 2>/dev/null || need pillow "$(py pillow)"
python3 -c "import playwright" 2>/dev/null || need playwright "$(py playwright) && python3 -m playwright install chromium"
command -v edge-tts >/dev/null || python3 -c "import edge_tts" 2>/dev/null || need edge-tts "$(py edge-tts)"
python3 - <<'PY' 2>/dev/null || need "chromium for playwright" "python3 -m playwright install chromium"
from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()
PY
D=$(cd "$(dirname "$0")/.." && pwd)
[ -f "$D/lib/three/build/three.module.js" ] || need "lib/three (Three.js r170)" "re-download the skill"
# optional (recommended): Whisper transcript QC + background removal for photo cut-outs
python3 -c "import mlx_whisper" 2>/dev/null || python3 -c "import whisper" 2>/dev/null || \
  echo "optional: $(py openai-whisper)   (qc_video.py transcript check; mlx-whisper on Apple Silicon is faster)"
python3 -c "import rembg" 2>/dev/null || echo "optional: $(py rembg)   (cut objects out of real photos)"
[ -f ~/.config/elevenlabs/api_key ] || [ -n "$ELEVENLABS_API_KEY" ] || echo "optional: ElevenLabs key not set (free edge-tts will be used unless the user provides one)"
command -v potrace >/dev/null || echo "optional: $(sys potrace)   (vectorize_logo.sh, crisp logos for beat edits)"
# other engines (Q1b) — only needed when the user picks them
node -e 'process.exit(+process.versions.node.split(".")[0]>=22?0:1)' 2>/dev/null || echo "optional: Node >= 22 (HyperFrames / Remotion engines) -> $(sys node)"
for s in hyperframes remotion-best-practices; do
  for d in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.omp/skills"; do
    [ -f "$d/$s/SKILL.md" ] && found=1
  done
  [ -n "$found" ] || { if [ "$s" = hyperframes ]; then echo "optional: HyperFrames skills -> npx -y hyperframes@latest skills update"; else echo "optional: Remotion skills -> npx -y skills add remotion-dev/skills -g -a claude-code -s remotion-best-practices -y"; fi; }
  unset found
done
[ $miss = 0 ] && echo "toolchain OK" || exit 1
