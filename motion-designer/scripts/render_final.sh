#!/bin/bash
# render_final.sh TIMELINE.html AUDIO.wav OUT.mp4 [AR=9x16] [SLICE_S=15]
# Machine-friendly final render: nice -n 15, 3 workers, rendered in slices; each slice is encoded (240 fps → 4-frame
# tmix motion blur → 60 fps) and its JPEG frames deleted immediately, so disk peaks at ~2 GB instead of ~7 GB.
# Then: concat, mux audio with loudnorm (−14.5 LUFS, TP −1), and an _upload.mp4 (CRF 22, ~50 MB/80 s) for posting.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); HTML=$1; WAV=$2; OUT=$3; AR=${4:-9x16}; SL=${5:-15}; FPS=240
SRC=$(cd "$(dirname "$HTML")" && pwd); TMP="$SRC/_slices"; rm -rf "$TMP"; mkdir -p "$TMP"; : > "$TMP/list.txt"
DUR=$(python3 - "$HTML" "$AR" <<'PY'
import asyncio, os, sys
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files', '--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
        pg = await b.new_page(); await pg.goto('file://' + os.path.abspath(sys.argv[1]) + '?ar=' + sys.argv[2])
        await pg.wait_for_function('window.ready===true', timeout=300000); print(await pg.evaluate('window.DUR')); await b.close()
asyncio.run(m())
PY
)
echo "DUR=$DUR s, slices of $SL s"; df -h "$SRC" | tail -1
for a in $(python3 -c "import math;print(' '.join(str(i*$SL) for i in range(math.ceil($DUR/$SL))))"); do
  b=$(python3 -c "print(min($a+$SL,$DUR)-0.5/$FPS)")
  nice -n 15 python3 "$HERE/render.py" "$HTML" --ar "$AR" --fps $FPS --workers 3 --range "$a,$b" --out "$TMP/f"
  nice -n 15 ffmpeg -y -loglevel error -framerate $FPS -start_number $((a*FPS)) -i "$TMP/f/%05d.jpg" \
    -vf "tmix=frames=4:weights='1 1 1 1',fps=60,format=yuv420p" -c:v libx264 -preset slow -crf 16 -profile:v high "$TMP/s$a.mp4"
  rm -rf "$TMP/f"; echo "file 's$a.mp4'" >> "$TMP/list.txt"; echo "slice $a done $(date +%T)"
done
nice -n 15 ffmpeg -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -c copy "$TMP/video.mp4"
nice -n 15 ffmpeg -y -loglevel error -i "$TMP/video.mp4" -i "$WAV" -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14.5:TP=-1.0:LRA=11 \
  -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$OUT"
nice -n 15 ffmpeg -y -loglevel error -i "$OUT" -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart -c:a copy "${OUT%.mp4}_upload.mp4"
rm -rf "$TMP"; ls -la "$OUT" "${OUT%.mp4}_upload.mp4"; echo "ALL DONE $(date +%T)"
