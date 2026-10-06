# Beat edit — the dossier

A **beat edit** (also called a *hype edit* or *velocity edit*) is a short vertical video driven entirely by a song:
every cut, word, zoom and shake lands on a beat; giant words carry the message; there is **no narration**. It is the
format people actually stop for on Reels/TikTok/Shorts — think phonk / funk / drill edits with slowed + reverb audio.

Everything here comes from real review rounds. Each rule exists because a draft without it was rejected.

---

## 1. What makes it work (the feel)
- **The music is the director.** Map the song first (`beat_map.py`), then design. Cuts that miss the beat are the
  fastest way to look amateur.
- **Speed.** A new visual on every bass hit (≈ 0.3–0.6 s). Nothing static for more than ~1 s. "Too much time standing
  still" and "a screen that means nothing" were the main rejections of an otherwise good draft.
- **Contrast: hold vs release.** The intro holds (readable setup), the drop releases (hero + rapid shots). After 3–4 s
  of rapid cuts, a 1–2 s moment that still MOVES (spinning hero, rain of particles) — never a frozen frame.
- **Few words, huge.** 1–3 words per slam, the accent colour on the punch word. The whole edit reads as ONE sentence
  chain (e.g. "STOP / SCROLLING. / THIS / CHANGES / EVERYTHING. / HERE'S HOW / …"). Paragraphs, cards full of copy and
  feature lists kill it ("too much text, too much information").
- **Edit, not ad.** Grain, shake, flashes, whips, slightly raw. Not "pretty". It should feel like a fan edit that happens
  to carry a brand.
- **Message with substance.** Even in slang, the words must say something real: what it is, what it changes, how it
  works (3–5 verbs), and the offer. Jokes the user threw out loosely ("the craziest app ever") are tone hints — write the real
  promise, don't paste the joke.
- **A clear offer at the end.** Marketing feedback on a strong draft was "great top of funnel — just improve the offer".
  Close with what the viewer gets and how (join the list / download / link), as a lockup + button.

## 2. Structure (adapt to the song — durations follow the music)
| part | when | what |
|---|---|---|
| **Opener** | intro of the song (before the drop) | a relatable setup: a recreated chat (2–3 messages max), a POV caption, a question — or straight to the hero if the song opens hard |
| **Dive** | last ~1.4 s before the drop | push into one element of the opener (a link preview, a logo), black out, the hero mark glowing alone |
| **Drop** | the drop (biggest bass rise) | the hero spins/flips/explodes, flash, particle burst |
| **Message** | hits after the drop | one 1–3 word slam per hit, each over a different moving visual |
| **How / proof** | middle | 3–5 verbs, one per hit, each with its own visual (phone tap, vehicle crossing, counter climbing, objects into a bag…) |
| **Offer** | before the lockup | what you get (an offer card with ✓ benefits), the referral / bonus, "JOIN" |
| **Burst** | ~1 s, once or twice | strobe: content switches every 4 frames (60 fps), alternating backgrounds |
| **Lockup** | last ~3 s of music | logo + URL + CTA button, particles, pulse on every hit |
| **Silent punchline** | after the music cuts (`quiet` in beats.json) | back to the opener's chat: a short reply that resolves the joke, then end |

Never copy the order of scenes or the lines of a reference edit — copy the rhythm and the language.

## 3. Intake (what to ask — see SKILL.md Flow C)
1. **Subject** — a brand/product (→ URL: logo, colours, real claims, offer) or a topic/person/event.
2. **The song** — the user downloads the audio file (mp3/wav/m4a) from wherever they get edit audios and drops it in
   the chat or gives a path. Ask for the section if the song is long ("from 0:42 to 1:15"). Treatment: slowed + reverb
   (classic) · original · sped up.
3. **The message** — the 3–8 phrases that must appear, or "write it for me" (then propose them in one list before
   building: hook slam → what it is → what it changes → how it works → offer → CTA).
4. **Opener** — recreated chat (WhatsApp, iMessage, Slack, Discord, Instagram DMs…) · POV/question caption · straight to the hero.
5. Versions (1–2 is plenty), platforms, ending (silent punchline / lockup only / loop to the start).
No narration, voice, captions or narration-engine questions — the song is the audio.

## 4. Audio pipeline
```bash
python3 $SKILL/scripts/slowed_reverb.py song.mp3 source/song.wav --speed .85 --wet .42      # slowed + reverb (0.8–0.9 typical)
python3 $SKILL/scripts/beat_map.py source/song.wav --out source/beats.json                 # → beats.json + beats.js
ffmpeg -i source/song.wav -af "apad=whole_dur=<DUR>" source/song_padded.wav                 # if the punchline runs past the song
```
- `beat_map.py` prints the bass hits (put every cut on one), the **drop** (hero reveal goes exactly there) and the
  **quiet** stretches (the pre-drop gap and the music cut → silent punchline). All times are snapped to 1/60 s.
- Slowed = pitch and tempo down together (`asetrate`), +5 dB at 70 Hz, a 3 s dark reverb (low-passed noise IR, 35 ms
  pre-delay). Analyse the *processed* file, never the original.
- Music the user supplies is their call; mention once that tracks from edit-audio libraries may still be copyrighted
  if the post becomes a paid ad.

## 5. Visual system
- **Palette** from the subject (brand colours from the site/CSS). Rotate 4–5 backgrounds (dark, main, accent, pop,
  light) so consecutive shots never share a background.
- **Type:** one condensed ultra-bold display (Anton/Bebas-like), uppercase, accent colour on the punch word, soft
  shadow so it reads over anything. UI text in the opener uses the system font (SF on macOS) for realism.
- **Hero mark:** something only this subject has (the symbol inside the logo, the product, the object). It spins,
  flips into a reward token, explodes. **Always vector or high-res**: a logo upscaled from a small PNG looks pixelated —
  run `scripts/vectorize_logo.sh logo.png assets/logo` (potrace) and draw from the SVG rasterised once at 2400 px.
- **Objects of the theme** (icons/illustrations from the site or open banks) orbit, rain, get sucked into a container,
  pop in on hits.
- **Reward token** (coin, star, heart…) for bursts and rain when the message involves value.
- **Offer card** (ticket / pass style) with 3 ✓ benefits taken verbatim from the site.
- Text-bearing visuals (phone mock, card, counter, vehicle) push the slam to the TOP (`hi` words) so nothing overlaps.

## 6. Motion kit (all in `templates/beat-edit.html`)
- **Pulse** on every hit: stage zoom +6%, shake ±8 px, tiny rotation, decaying over ~130 ms.
- **Whip-in** for every new shot: canvas slides in from alternating sides with blur over ~0.09 s.
- **Slam** words: overshoot scale 1.45 → 1 in 0.12 s.
- **Flash** frames on the drop / logo / bursts.
- **Strobe:** content changes every 4 frames — index from `round(u*60)/4`, never `floor(u*15)` (unaligned changes get
  blended by tmix and look washed out).
- **Grain** overlay (deterministic per frame), rotating background rays, radial glow.
- Particle physics are pure functions of time (`hash(k)` for randomness) so every render is identical.

## 7. Recreated chat opener (real-app fidelity)
A chat that "looks AI-made" ruins the hook. Make it indistinguishable from a screenshot:
- **Look at the real app first.** Open it on this Mac and capture ONLY its window
  (`screencapture -x -o -l <windowid>`; find the id with a tiny Swift `CGWindowListCopyWindowInfo` script), sample
  colours/spacing, then **delete the screenshot** — never put real names or messages in the video.
- Phone-format UI (status bar, header with group avatar/name/members, wallpaper doodles, bubbles with coloured sender
  names, time stamps, reactions, link preview card, input bar with mic). System font, real emoji.
- **2–3 messages**, each on an intro hit, held long enough to read. A crowded chat is unreadable at speed.
- Bubbles sit right above the input bar (stack from the bottom). New message → **snap** the feed, never animate the
  scroll (fast scroll + motion blur = ghost copies).
- "X is typing…" in the header before each message; a reaction pops a beat later.
- The link preview (logo + promise + domain) is the bridge into the dive.

## 8. Render + QC
- `render_final.sh beat-edit.html song_padded.wav out.mp4 9x16 9` (240 fps → tmix=4 → 60 fps, sliced, + `_upload.mp4`).
- Guard every radius/size that eases from 0 (`if(!(r>1))return`) — an overshoot easing can go a hair below zero and
  crash the canvas mid-render.
- QC at 3 fps sheets: every shot different from its neighbours, no static stretch > 1 s, words never over other text,
  strobe colours solid, logo crisp, chat readable. Then listen: drop on the hero, cuts on hits, silence on the punchline.

## 9. Checklist before showing it
- [ ] Cuts on bass hits; hero exactly on the drop; punchline in the silence
- [ ] New visual every hit after the drop; nothing frozen > 1 s
- [ ] ≤ 3 words per slam; one sentence-chain message; real claims only
- [ ] Clear offer + CTA lockup at the end
- [ ] Opener chat looks like the real app; 2–3 messages; no real personal data
- [ ] Logo vector-crisp; strobe aligned to 4-frame steps; grain on
