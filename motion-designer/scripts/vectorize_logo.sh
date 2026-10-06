#!/bin/bash
# vectorize_logo.sh logo.png OUT_PREFIX [#hexcolor ...]
# Turns a raster logo (the usual PNG from a website) into a crisp SVG with potrace, so it can be scaled to full screen
# without pixels. Writes OUT_PREFIX-white.svg, OUT_PREFIX-black.svg and one file per extra colour given.
# Needs: brew install potrace. Works for flat single-colour marks; for multi-colour logos trace each colour separately.
set -e
SRC=$1; OUT=$2; shift 2
command -v potrace >/dev/null || { echo "potrace missing -> brew install potrace"; exit 1; }
python3 - "$SRC" "$OUT.bmp" <<'PY'
import sys
from PIL import Image, ImageFilter
im = Image.open(sys.argv[1]).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
g = bg.convert('L')
# logo darker than white → ink; if the logo is white-on-transparent, invert first
if sum(g.getdata()) / (g.width * g.height) > 250: g = Image.eval(im.split()[3], lambda v: 255 - v)
g = g.resize((g.width * 6, g.height * 6), Image.BICUBIC).filter(ImageFilter.GaussianBlur(7))
g.point(lambda v: 0 if v < 135 else 255).convert('1').save(sys.argv[2])
PY
potrace "$OUT.bmp" -s -o "$OUT-trace.svg" --turdsize 60 --alphamax 1.25 --opttolerance 1.0; rm -f "$OUT.bmp"
sed 's/fill="#000000"/fill="#ffffff"/' "$OUT-trace.svg" > "$OUT-white.svg"; cp "$OUT-trace.svg" "$OUT-black.svg"
for c in "$@"; do sed "s/fill=\"#000000\"/fill=\"$c\"/" "$OUT-trace.svg" > "$OUT-${c#\#}.svg"; done
rm -f "$OUT-trace.svg"; ls -1 "$OUT"-*.svg
