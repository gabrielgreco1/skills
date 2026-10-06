#!/bin/bash
# encode.sh FRAMES_DIR AUDIO.wav OUT.mp4 [FPS_IN=240]
# 240 fps frames -> tmix (4-frame motion blur) -> 60 fps H.264 + AAC, loudness-normalized for social (-14.5 LUFS).
# For 30 fps drafts pass FPS_IN=30 (no blending).
set -e
F=$1; A=$2; O=$3; FPS=${4:-240}
if [ "$FPS" -ge 120 ]; then K=$((FPS/60)); W=$(printf '1 %.0s' $(seq 1 $K)); VF="tmix=frames=$K:weights='${W% }',fps=60,format=yuv420p"
else VF="format=yuv420p"; fi
mkdir -p "$(dirname "$O")"
# loudnorm on a fully silent track produces NaN -> skip normalization for silent audio
PEAK=$(python3 -c "import wave,sys,numpy as n;w=wave.open(sys.argv[1]);print(int(n.abs(n.frombuffer(w.readframes(w.getnframes()),n.int16)).max(initial=0)))" "$A")
AF="-af loudnorm=I=-14.5:TP=-1.0:LRA=11"; [ "$PEAK" = "0" ] && AF=""
ffmpeg -y -loglevel error -framerate "$FPS" -i "$F/%05d.jpg" -i "$A" \
  -filter_complex "[0:v]$VF[v]" -map "[v]" -map 1:a \
  -c:v libx264 -preset slow -crf 16 -profile:v high -tune animation -movflags +faststart \
  $AF -c:a aac -b:a 320k -ar 48000 -shortest "$O"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height,r_frame_rate -of compact "$O"
