# Production pipeline

Deterministic HTML/SVG timeline → Playwright frame capture at 240 fps → ffmpeg 4-frame `tmix` (real motion blur) →
60 fps H.264 + numpy-synthesized, event-locked soundtrack + edge-tts narration. No After Effects, no stock assets,
fully reproducible: re-render any slice after a fix.

`$S` below = this skill's `scripts/` folder. Run `$S/check_env.sh` once per machine.

## Project layout
```
~/Desktop/<product>-motion/<NN>-<slug>/
  README.md                    # concept, one-sentence story, versions, status, rejection notes
  options/A-<angle>/           # one folder per version (made by independent agents)
    source/timeline.html       # the video (copy of templates/timeline.html)
    source/audio.py            # soundtrack (imports sfx.py)
    source/vo/lines.tsv        # narration cues (if narrated)
    A-<angle>_<platform>_<W>x<H>.mp4   # draft for review (first selected platform)
  final/
    sound/<slug>_<platform>_<W>x<H>.mp4      # e.g. _linkedin_1080x1080, _instagram_1080x1350, _x_1920x1080, _reels_1080x1920
    narrated/<slug>_<platform>_<W>x<H>.mp4
    silent/ · vo-only/         # only if requested
```

## 3D in the timeline (Three.js, offline)
Add to `timeline.html` (absolute paths so renders work offline; the page must be a `type="module"` script):
```html
<script type="importmap">{"imports":{"three":"file://$SKILL/lib/three/build/three.module.js",
                                     "three/addons/":"file://$SKILL/lib/three/examples/jsm/"}}</script>
<script type="module"> import * as K from 'file://$SKILL/templates/three-kit.js'; /* see the header of three-kit.js */ </script>
```
Load HDRIs/GLBs/textures through the kit (`G.hdr/G.glb/G.tex`) — `fetch()` of file:// is blocked even with the
render flag. Expose `window.FOCAL_BOXES=()=>[G.box(obj,cam,'name')]` so the layout check sees 3D heroes. Await every
load before `window.ready=true`. One WebGL canvas for all 3D scenes; switch scenes in `seek(t)`.

## Steps
1. **Copy** `templates/timeline.html` → `source/timeline.html`. Replace the BRAND block with the exact tokens
   (colors, fonts via Google Fonts or `@font-face` to local files, logos inlined as SVG or base64).
2. **Build scenes** as functions of `t` only (no `Date.now`, no CSS transitions/animations, no `Math.random` — use `hash(n)`).
   Name every important moment in `MARK` (cuts, lands, taps, CTA) — audio and VO lock to these.
3. **Layout per format** in `LAYOUT` (16x9, 1x1, 4x5, 9x16, plus any custom `WxH` the user asked for). Compose each
   one (stack vertically on tall formats). Platform map: LinkedIn post 1x1 · Instagram post 4x5 · X/Twitter 16x9 ·
   Reels/TikTok/Shorts/Stories 9x16 · YouTube 16x9.
   Debug live: `open "timeline.html?ar=9x16&guides=1&play=1"`.
4. **Check stills yourself**: `python3 $S/render.py source/timeline.html --ar 16x9 --test 0.5,2,4,6,9,12,15` →
   look at `test_16x9/sheet.png` (Read the PNG). Check readability, overflow, alignment, brand. Repeat per format.
   The run also prints layout problems (OUTSIDE SAFE ZONE · TEXT OVERLAP · TEXT OVER IMAGE · CUT OFF BY FRAME) — it
   must say `layout: OK`. Derive every position from `SB`/`ZONES` (safe box → HEAD · VIS · CAP bands), never from the
   frame edges; mark hero visuals `data-role="focal"` (3D: `window.FOCAL_BOXES`). Before the final render run the
   whole-timeline check: `python3 $S/render.py source/timeline.html --ar 9x16 --sweep 10` (exit code 1 on problems).
5. **Marks**: `python3 $S/export_marks.py source/timeline.html > source/marks.json`.
6. **Sound**: write `source/audio.py`:
   ```python
   import sys; sys.path.insert(0, '<S>'); from sfx import *
   M = marks('marks.json'); init(M['DUR'])
   groove(0, M['END'], bpm=120)            # light bed
   put(whoosh(.8), M['T2'] - .3, .45)      # every SFX on a visual event
   put(boom(), M['END'], .8, verb=.4)
   master('sound.wav'); silence('silent.wav', M['DUR'])
   ```
7. **Narration** (if requested) — ElevenLabs: write `source/vo/script.txt` (one paragraph per act, craft.md §7 rules),
   `python3 $S/el_tts.py source/vo/script.txt --voice <id> --budget <credits> --only 0` (test), then without `--only`.
   It writes `vo/narration.wav` + `vo/words.json` ({w,s,e} per word) → lock MARKs to those times and feed the words to
   `Captions()`; mix with `mix.py` (or ffmpeg sidechain) keeping music −9 dB under the voice.
   edge-tts: `source/vo/lines.tsv` = `start<TAB>end<TAB>text` per cue (windows from marks).
   `python3 $S/vo.py source/vo/lines.tsv --voice <the user's pick: female-us | male-us | female-ptbr | male-ptbr>` — fix every flagged overrun.
   Mix: `python3 $S/mix.py --dur <DUR> --music sound.wav --vo vo/lines.tsv --out narrated.wav`
   (VO only: omit `--music`, out `vo-only.wav`).
8a. **Assets**: `python3 $S/fetch_assets.py <threejs|commons|polyhaven|nasa> … --out <root>/assets`, then
   `python3 $S/prep_image.py card|cutout|grade|grain …`.
8. **Draft** (fast, for direction, in the first selected platform's size):
   `python3 $S/render.py source/timeline.html --ar 1x1 --fps 30 --scale .5 --out frames_draft`
   then `$S/encode.sh frames_draft sound.wav ../A-<angle>_linkedin_1080x1080.mp4 30`.
9. **Final** — one format: `$S/render_final.sh source/timeline.html source/narrated.wav <out>.mp4 9x16` (sliced, low-impact,
   + `_upload.mp4`). Several formats/variants: `$S/render_all.sh source/timeline.html <root>/final <slug> "linkedin:1x1 instagram:4x5 x:16x9 reels:9x16" "sound narrated"`
   (~20 s render per 14 s of 1:1 video on an M-series Mac; 240 fps × 4 formats is the slow part).
10. **Patch** a fix without re-rendering everything: `render.py ... --range 12.0,14.5 --out frames_16x9` then re-encode.
11. **QC** (every final render — craft.md §9):
    `python3 $S/qc_video.py <mp4> --vo source/vo/narration.wav --words source/vo/words.json --script source/vo/script.txt`
    (audio offset · Whisper transcript diff · pauses · black/white/frozen frames · loudness · 4 fps sheets in `qc_out/sheets/`)
    `python3 $S/qc_captions.py source/timeline.html --ar 9x16` (caption position stable at 60 fps · hold · on-time)
    Read every sheet; fix → patch-render → re-run until clean.
12. **Reveal**: `open -R <file>` for each deliverable (or `open <folder>`).

## Machine etiquette
Run renders as `nice -n 15 python3 $S/render.py … --workers 3`, in slices (`--range`) for long videos, and delete
the 240 fps frames right after encoding (≈ 6–7 GB per minute of 9:16). Never run three full renders at once.

## Gotchas
- Wait for fonts: the template awaits `document.fonts.ready`; external fonts need network during render.
- Artifact/HTML CSP isn't an issue here (local file), but keep assets local/inlined so renders are reproducible offline.
- Use `vector-effect` carefully: with camera scale, prefer stroke widths in drawing units so motion stays deterministic.
- `--force-color-profile=srgb` is set in render.py so brand hexes come out exact.
- JPEG q94 frames keep disk use sane (~1–2 GB per 30 s format at 240 fps); `render_all.sh` deletes frames after encoding.
