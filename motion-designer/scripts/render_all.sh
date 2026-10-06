#!/bin/bash
# render_all.sh TIMELINE.html OUT_DIR SLUG "linkedin:1x1 instagram:4x5 x:16x9 reels:9x16" "sound narrated"
# Renders each requested size natively (the page lays itself out per ?ar=) once, then muxes every audio
# variant (expects <variant>.wav next to the timeline: silent / sound / narrated / vo-only).
# Several platforms may share one size: it is rendered once and saved under each platform name.
# Output: OUT_DIR/<variant>/<SLUG>_<platform>_<W>x<H>.mp4
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
HTML=$1; OUT=$2; SLUG=$3; SPECS=${4:-"linkedin:1x1 instagram:4x5 x:16x9 reels:9x16"}; VARS=${5:-"sound"}
SRC=$(cd "$(dirname "$HTML")" && pwd)
size() { case $1 in 16x9) echo 1920x1080;; 1x1) echo 1080x1080;; 4x5) echo 1080x1350;; 9x16) echo 1080x1920;; *) echo $1;; esac; }
for AR in $(for s in $SPECS; do echo ${s##*:}; done | sort -u); do
  rm -rf "$SRC/frames_$AR"
  python3 "$HERE/render.py" "$HTML" --ar "$AR" --fps 240 --out "$SRC/frames_$AR"
  for s in $SPECS; do
    [ "${s##*:}" = "$AR" ] || continue; P=${s%%:*}
    for V in $VARS; do "$HERE/encode.sh" "$SRC/frames_$AR" "$SRC/$V.wav" "$OUT/$V/${SLUG}_${P}_$(size $AR).mp4"; done
  done
  rm -rf "$SRC/frames_$AR"; echo "done $AR"
done
