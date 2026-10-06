# Beat edit — the format

A **beat edit** (also called a *hype edit* or *velocity edit*) is a short video driven by a song: every cut, word,
zoom and shake lands on a beat, giant words carry the message, and there is **no narration**. It's the phonk / funk /
slowed + reverb edit style people stop for on Reels, TikTok and Shorts.

This file is about the **format**: how the music drives the motion. The content (what appears, how it opens, how it
ends) is invented fresh for every video from the idea. Never reuse a previous edit's script, opener or ending.

Every rule below comes from a real review round.

---

## 1. The feel
- **The music is the director.** Map the song before designing anything (`beat_map.py`). A cut that misses the beat
  is the fastest way to look amateur.
- **Speed.** A new visual on every bass hit after the drop (≈ 0.3–0.6 s each). Nothing frozen for more than ~1 s.
  "Too much time standing still" and "a screen that means nothing" sank an otherwise good draft.
- **Hold vs release.** Before the drop: tension (dark, slow push, a pulse on the intro hits). On the drop: release
  (flash + hero + burst). After 3–4 s of rapid shots, a 1–2 s breath that still MOVES (spinning hero, particle rain),
  never a still frame.
- **Few words, huge.** 1–3 words per slam, the accent colour on the punch word. Read in order, the slams form ONE
  sentence chain (e.g. "STOP / SCROLLING. / THIS / CHANGES / EVERYTHING."). Paragraphs, feature lists and cards full
  of copy kill it: "too much text, too much information".
- **Raw, not pretty.** Grain, shake, flashes, whips. It should feel like a fan edit, even when it carries a brand.
- **Words with substance.** Slang is fine, but the slams must say something real about the subject. A joke the user
  throws out loosely is a tone hint, not copy.
- **For a brand, the last seconds sell.** Say what the viewer gets and how (logo + URL / handle + a clear action).
  "Great top of funnel, just improve the offer" was the note on a draft that ended without one.

## 2. Anatomy (the song decides the lengths)
| section | where in the song | job |
|---|---|---|
| **Build-up** | intro, before the drop | tension and context: whatever fits the idea (a dark hero pulsing on the intro hits, a hook caption, an object, a scene) |
| **Drop** | the biggest rise in bass energy (`drop` in beats.json) | flash + the hero reveal: spin, flip, explode, burst |
| **Run** | hits after the drop | one shot per hit, each with its own visual + a 1–3 word slam |
| **Breath** | 1–2 s, once or twice | the hero big and moving, no words or one word, so the eye rests without stopping |
| **Burst** | ~1 s, before a key moment | strobe: the content switches every 4 frames at 60 fps, alternating backgrounds |
| **Close** | the last bar | the payoff: logo/title slam, URL or handle, the action, pulsing on the hits |
| **Silence** (optional) | a `quiet` stretch where the music cuts | one last beat in silence. Very strong when the idea has a punchline. |

Short songs or sections (8–15 s) can be drop → run → close. Longer ones (45–60 s) can have two drops with a break
between. Never copy a reference edit's order of scenes or its lines. Copy the rhythm and the language.

## 3. Audio pipeline
```bash
python3 $SKILL/scripts/slowed_reverb.py song.mp3 source/song.wav --speed .85 --wet .42      # slowed + reverb (0.8–0.9 typical)
python3 $SKILL/scripts/beat_map.py source/song.wav --out source/beats.json                 # → beats.json + beats.js
```
- `beat_map.py` prints the bass hits (one shot per hit), the **drop** (the hero goes exactly there) and the **quiet**
  stretches (pre-drop gap, music cut). Every time is snapped to 1/60 s.
- Slowed = pitch and tempo down together, +5 dB at 70 Hz, a 3 s dark reverb. Always analyse the *processed* file.
- Use `--start/--dur` to take a section of a long song. Pad with `apad` if the video runs past the audio.
- The user supplies the song. Mention once that edit audios can still be copyrighted if the post becomes a paid ad.

## 4. Visual system
- **Palette** from the subject (brand CSS, the topic's world). Rotate 4–5 backgrounds so neighbouring shots never
  share one.
- **Type:** one condensed ultra-bold display face (Anton / Bebas-like), uppercase, punch word in the accent colour,
  soft shadow so it reads over anything.
- **Hero:** the thing only this subject has (the symbol in the logo, the product, the iconic object or photo). It
  carries the build-up, the drop and the close. **Always crisp**: a logo upscaled from a small PNG looks pixelated, so
  run `scripts/vectorize_logo.sh logo.png assets/logo` (potrace). The template rasterises SVGs once at high resolution.
- **Supporting images:** objects, photos, frames, icons of the theme. They orbit, pop in, fill the frame with a
  punch zoom, swap in pairs, rain as particles.
- When a visual carries its own text (a UI mock, a counter), the slam moves away from it. Two texts never overlap.

## 5. Motion kit (`templates/beat-edit.html`)
| effect | spec |
|---|---|
| **Pulse** | on every hit: stage zoom +6 %, shake ±8 px, rotation ±0.6°, decaying in ~130 ms |
| **Whip-in** | every new shot slides in from alternating sides with blur, over ~0.09 s |
| **Slam** | words overshoot from 1.45× to 1× in 0.12 s |
| **Flash** | white frames on the drop and on hero hits |
| **Strobe** | content index = `round(u*60)/4`. Never `floor(u*15)`: unaligned switches get blended by tmix and look washed out |
| **Grain** | a per-frame noise overlay, plus rotating background rays and a radial glow |
| **Determinism** | every particle and shake is a pure function of time (`hash(k)`), so every render is identical |

Visual vocabulary in the template: `buildup`, `flip`, `burst`, `orbit`, `rain`, `spin`, `slam`, `pop`, `photo`,
`split`, `strobe`. Add new ones per idea: the vocabulary is a starting set, not a menu to stay inside.

## 6. Build
1. Map the song, then write the shot list on paper: one line per hit (time · visual · words). Read the words in order
   as one sentence.
2. Copy `templates/beat-edit.html` into `<root>/source/` with `beats.js`, the song and the images. Set `CFG` (palette,
   accent, hero, images) and write `SHOTS_SRC` for this idea (`'drop'`, `'hit+N'`, `'hit:N'`, `'end-1.5'` or seconds).
3. `render.py --test` on ~15 stills across the timeline, then fix overlaps and empty frames.
4. `render_final.sh beat-edit.html source/song.wav <out>.mp4 9x16` (240 fps → tmix 4 → 60 fps, plus `_upload.mp4`).
5. QC with a 3 fps contact sheet of the MP4: every shot differs from its neighbours, nothing static, words readable,
   strobe colours solid, hero crisp.

Guard anything that eases up from zero (`if(!(r>1))return`): an overshoot easing can dip a hair below zero and crash
the canvas mid-render.

## 7. Checklist
- [ ] Cuts on bass hits, hero exactly on the drop
- [ ] A new visual every hit after the drop, nothing frozen for more than 1 s
- [ ] ≤ 3 words per slam, forming one sentence chain, real claims only
- [ ] Opener and ending written for this idea, not reused
- [ ] Hero crisp (vector), strobe aligned to 4-frame steps, grain on
- [ ] For a brand: a clear close (what you get + where)
