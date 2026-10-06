# Craft rules — the quality bar

These rules come from real review rounds on short product videos. Each one exists because a draft was rejected
without it. Check all of them before showing a video.

## 1. Story before visuals
- Write the plot so a stranger could retell it in **one sentence**. If you can't, don't animate yet.
- The first ~3 s must state **what is at stake and why** (where we are, what the thing is, what the risk/payoff is).
  A vague slogan as the hook fails even with great visuals: if the viewer asks *"what is this about? what's at risk?"*,
  the story is missing context.
- Open with a **title card that names the concept** when the format is a meme/parody (e.g. "SPEEDRUN — any%").
- Shareable shorts must **not look like ads**: the joke/format leads, the product appears as the answer, not as a banner.
- Every video **ends by saying what the product solves + one clear CTA** (in-world, not salesy). A strong short with
  an unclear CTA gets sent back.

## 1b. Narration-first: design the picture TO the voice
For narrated videos the script and the real voice come FIRST and drive the design. Designing visuals first and squeezing the voice in afterwards was rejected.
1. Write a two-column script — **voice | picture**: every sentence next to exactly what the viewer sees while it's
   spoken. The picture shows what the words say at that moment; the words point at the picture ("look at this", "this one here").
2. Generate the final voice (ElevenLabs `el_tts.py`, or edge-tts) → `words.json` with the time of every word.
3. Build the beat sheet from those word times: cuts, reveals, camera moves, counters, callouts and SFX each keyed to a
   spoken word. Shot length = the voice's rhythm. Need more picture time? Add a breath between sentences in the script.
4. Then style frames and animation at the real timestamps (a 30 fps half-res animatic with the voice is the first check).

## 1c. Hook + retention — keep them to the last second
The goal of a short is that people watch to the end. Pick the hook in the intake (Q13) and build every act around it.
- **Hook patterns** (frame 0 already shows it — big, real, readable):
  · *Relatable moment* — something the viewer did 5 seconds ago, made the hero: a tap, a message or a purchase
    that becomes the first frame of the story ("That thing you just did took <surprising fact>").
  · *Before/after contrast* — a real photo of the past vs the present (an archive photo → the same thing today).
  · *Flash-forward* — show the most surprising image first, then "let's rewind".
  · *Shock number/claim* — one verified number, huge, with a real image ("<one surprising, sourced number>").
- **Open loop (retention tease)** for videos > 40 s: in the first ~12 s promise a payoff that only comes at the end
  ("The first version only lasted three weeks. I'll tell you why.") and pay it off explicitly near the end
  ("Three weeks later it failed, because <reason>"). Then close the loop back to the hook image.
- **Re-hook every 6–10 s**: a question ("So what's inside?"), a reveal, a scale jump, a local angle ("and your country is
  on this map"), a myth vs fact ("everyone blames X — the real culprit is Y").
- **The CTA is part of the story's end**, said by the narrator and shown on a designed end card (Q9).

## 2. Readability (the #1 rejection reason)
- **One main read path per screen.** If the eye has to choose between a prop, a screen, a background and a caption, it's wrong.
- **Hold every text ≥ words/3 + 1 s** (`hold()` in the template). People need time to see and read — never jam slides.
- Prefer **longer and clearer over shorter and dense**: more seconds, one item at a time.
- Cut every KPI / panel / label that doesn't serve the story — decorative numbers confuse.
- Minimum type size on 1080-wide formats ≈ 34 px body, 28 px mono labels. Headlines ≥ 96 px.
- Numbers: tabular figures, right-aligned, with padding; timers/counters must never look crooked or jitter.

## 3. Composition
- **Nothing leaves its container**: check frame-by-frame that no element spills out of a card, device frame or cam window.
- **No stick figures / drawn humans.** Represent people through actions: a cursor labelled "you", typing, a back-view
  silhouette, laptop lids, lower-third chyrons, a single lit window at night.
- Keep the frame alive with a **slow camera push** (1.00 → 1.04) rather than extra elements.
- Transitions are motivated (whip-pan, match-cut, zoom into a detail) — not random wipes. Never a flat grey/white frame
  between shots: dip through the scene's own dark colour (~0.4 s), zoom-through, match cut.
- **Motion pacing is an intake choice (Q15)** — cut rhythm always follows the narration; the preset sets motion INSIDE shots:
  · *Calm & cinematic* (audience feedback on a posted 3D reel: "animations too fast — not slow, just not THAT fast"):
    camera moves span the whole shot with in-out easing (≈ ≤ 20°/s rotation, push ≤ 1.00→1.08), exploded views 1.5–2.5 s
    then HOLD ≥ 1 s, entrances/exits 0.5–0.8 s, transitions 0.6–1.0 s, flashes only at act changes, one major movement
    at a time, counters roll ≥ 1.2 s and land on the spoken number.
  · *Dynamic*: snappier entrances (0.3–0.4 s), whips on beats, faster counters — memes, showreels, music-driven cuts.
  Test either way: if your eye has to chase a move, it's too fast.

## 4. Brand fidelity
- Use the product's **real UI, colors, fonts and components** — pull them from the live site/code, never approximate.
- When parodying another medium (terminal, movie trailer, game HUD, chat), **re-skin it in the brand system**
  (e.g. a terminal rendered in the brand's background and type, not a generic black terminal). A parody with no
  brand identity reads as off-brand and gets rejected.
- Data visualizations must match the site's **exact patterns** (table row layout, bars, tiers, colors). Don't invent
  decorations the site doesn't use (badges, flags, arrows) — an invented chart style looks random.
- Use real data from the site. Never invent rankings, scores or stats. Quote stats verbatim with their source page.
- **Honest labels**: a caption must name exactly what the image shows. Don't call a photo of one chip/product/place
  another one (last year's model labelled as the new one), and don't label a generic 3D model as a specific real thing. If the exact
  image doesn't exist with a usable licence, label it generically ("a modern smartphone chip") or rebuild it in 3D.
- Respect the brand's forbidden claims (e.g. pricing/"free" promises that are outdated). Grep the copy before rendering.

## 5. Formats — native, never padded
Deliverables are chosen per platform in the intake (mobile-first):
| platform | ar | size | notes |
|---|---|---|---|
| LinkedIn post | 1:1 | 1080×1080 | 4:5 also works on LinkedIn mobile |
| Instagram post | 4:5 | 1080×1350 | best mobile feed footprint |
| X / Twitter post, YouTube | 16:9 | 1920×1080 | |
| Reels / TikTok / Shorts / Stories | 9:16 | 1080×1920 | keep text out of the bottom ~250 px (UI overlay) |
Each format is **composed from scratch** (per-format LAYOUT in the timeline). Never center a 16:9 render on a blurred
or padded background — videos must be generated natively at each size.

## 5b. Platform safe zones — keep it centred, keep it light
Social apps draw their own UI over the video (top bar, right-side action buttons, caption + CTA block at the bottom,
progress bar). Content glued to the edges gets covered or feels cramped and is hard to read.
| format | keep text/logos/CTA inside (px from edge: top · right · bottom · left) |
|---|---|
| 9:16 Reels/TikTok/Shorts/Stories | 260 · 150 · 460 · 150 → usable box ≈ 780×1200, centred |
| 4:5 feed | 110 · 90 · 120 · 90 |
| 1:1 feed | 90 · 90 · 90 · 90 |
| 16:9 | 80 · 110 · 90 · 110 |
- Only backgrounds/textures may bleed to the edge (mark them `data-bleed`).
- Tall formats: **centred, stacked, fewer elements** — one headline + one visual per screen. Cut content rather than
  shrink it or push it toward the edges; split a dense screen into two beats instead.
- `render.py --test` checks every visible text against the safe box and lists offenders — fix all before encoding.
  Preview the zones with `timeline.html?ar=9x16&guides=1` (tinted area = covered by app UI).

## 5c. Fit — every element in its own slot (no stacking, nothing cut)
"I'm not asking for less on screen — I'm asking for it to be well fitted." Overlaps read as broken even when each layer
is beautiful: captions over the photo, a kicker behind the headline, a number sliding under a label, an object half
outside the frame.
- **Three bands per screen** (template `ZONES`, inside the safe box): `HEAD` (kicker + headline) · `VIS` (the hero
  photo/3D/chart) · `CAP` (captions). Bands never overlap. The hero visual is sized with `fit(ZONES.VIS, aspect)` —
  contain, never crop. Need more content? Use **two screens**, not two layers.
- **Captions only in `CAP`.** Never over a photo, a 3D object, a chart or a headline. While a headline is speaking the
  same words, hide the caption (don't print the sentence twice).
- **Text over an image only when the image is a full-bleed background** (`data-bleed`) with a scrim, marked
  `data-over`. Hero objects (`data-role="focal"`, or `window.FOCAL_BOXES()` for 3D) must stay clear of all text.
- **Kickers/labels are positioned from the headline's measured box** (`getBoundingClientRect`, ≥ 24 px gap), never at a
  fixed y that a longer headline can run into. Callout labels sit beside the object with a leader line, inside `VIS`.
- **Nothing important is cut by the frame edge**: objects either fully inside, or deliberately full-bleed backgrounds.
  Hold the camera so the subject is whole at the end of every move, not only at the start.
- **Exits finish before entries start**: a headline/number leaving must be gone before the next one lands in the same
  band (mid-transition overlaps count too).
- **Verify**: `render.py --test …` and the whole-timeline `render.py --ar 9x16 --sweep 10` must print
  `layout: OK` (safe zone · no text overlap · no text over images · nothing cut). Fix every listed instant.

## 6. Sound
- Every SFX is tied to a visual event (cut, land, tap, stamp, count). Bed = light groove under the visuals.
- Loudness normalized to −14.5 LUFS (encode.sh does it).

## 7. Narration
**Writing for TTS (any engine)** — most "robotic" narration is a writing problem: conversational lines, questions,
short punchy sentence after a long one, numbers and acronyms spelled the way they're spoken. **No "..." or commas in
the middle of a sentence** ("Essa sala inteira, .., era um computador" was rejected — it must flow in one breath);
pauses only BETWEEN sentences; emphasis with CAPS on one word.
**Captions follow the speech**: each word appears at its spoken timestamp (unspoken words invisible), newest word in
accent; headlines that repeat the VO build word by word the same way (template `Captions()` + word timings).

**ElevenLabs (preferred when the user has a key)** — `scripts/el_tts.py`, key in `$ELEVENLABS_API_KEY` or
`~/.config/elevenlabs/api_key`. Approved recipe: `eleven_v3`, stability 0.3, similarity 0.8, seed 7 (`--pvc-as-ivc`
for professional voices); one chunk per act; audio tags (`[curious]`, `[excited]`, `[whispers]`, `[mischievously]`)
only at 3–5 turning points. Credits are scarce: listing voices and their previews is free — let the user pick from
previews; A/B one short line (≈150 credits/take) before the full read; set `--budget`; never regenerate cached chunks.
v3/v4 reject `previous_text`; they return character alignment (tags included → stripped by el_tts.py).
Free plans can't use library voices via API and have no commercial licence — say so before generating.
Never use library voices that imitate real celebrities without authorization.

**One continuous take** (best continuity): generate the WHOLE script in ONE ElevenLabs request (v3 ≤ 5,000 chars;
paragraph breaks = act breaks) instead of one request per act — separate requests change energy/pitch at every join.
Split it into cues with the alignment afterwards. If one line comes out wrong (a misread that changes the meaning, a
doubled syllable on a keyword), regenerate only that line and splice it **at a scene cut**, loudness-matched.
Typical cost: ~1 credit per character (an 80 s script ≈ 1,300 credits) — test the hook line first (~150 credits).
**Always transcribe the result** (`qc_video.py`, Whisper) and diff it against the script before building the picture:
a take can misread a sentence so its meaning flips (a misplaced comma, a word read as a different word) — often
only the transcript catches it. Check pauses > 0.35 s inside sentences in the word timings.

**Caption rules** (template `Captions()`, verified by `qc_captions.py` — every one of these was a visible bug):
- A chunk's layout is **static**: all its words are laid out when it appears (unspoken ones at opacity 0) — never
  add/remove words or re-centre while it's on screen (words jumped sideways and ghosted).
- Words a headline prints at the same moment are decided ONCE (a static hide set), never per frame.
- Chunks: one line, 2–4 words, never cross a sentence end, never split a spoken number ("noventa e oito palavras"),
  keep the script's punctuation; the last word stays readable ≥ ~0.3 s; a chunk leaves when the next spoken word
  starts — it never lingers over the next shot.
- Preload every font weight before `window.ready` — a weight first used mid-video loads late and re-flows the text.
- Caption plate = soft rounded backing behind the words only, never a full-width dark bar.

**edge-tts (free fallback)**
- **edge-tts**, American Multilingual neural voice, **rate +8%**, **no pitch shift**, **dry (no reverb/echo)**, silences trimmed,
  music ducked −9 dB under the voice. Voices (user picks — no default gender): female `en-US-AvaMultilingualNeural`, male `en-US-AndrewMultilingualNeural`;
  pt-BR female `pt-BR-ThalitaMultilingualNeural`.
- Avoid: slow rate (−14%), pitch shifts, room reverb — they sound sluggish and echoey.
- Write VO to the timeline windows (`vo.py` flags overruns). Fix the script or hold the shot longer — don't speed the voice up.
- edge-tts uses a Microsoft endpoint without formal commercial terms: mention this if the video will run as a **paid ad**,
  and offer ElevenLabs (or whatever the user prefers) instead. If the user names a better TTS, use it and record it.

## 8. Real assets, real hook, design first
Flat SVG icons floating in an empty frame were rejected as "AI-looking, badly made, no hook".
- **Hook = curiosity gap + a striking real image in frame 0** (flash-forward to the payoff, "how is that possible?",
  "only one company in the world can…"). Never open on context, a date or a logo.
- **Real photos and real 3D**: Wikimedia Commons (PD/CC), NASA/NIH (PD), Fritzchens Fritz (CC0 die shots), Poly Haven
  (CC0 HDRIs/models/textures), Smithsonian 3D (CC0). Record license + attribution per file; CC BY/BY-SA credits go in
  the post caption. Animate them: parallax layers, cut-outs (rembg), Three.js PBR objects lit by an HDRI, exploded
  views, callouts with leader lines, light sweeps, grain.
- **Asset banks that worked** — fetch with `scripts/fetch_assets.py` (logs licence + attribution per file in `catalog.md`): the **three.js examples library** (ready glTF models such as DamagedHelmet/BoomBox/IridescenceLamp, NASA Earth day/night/specular textures, Poly Haven HDRIs — `fetch_assets.py threejs --list`; https://threejs.org/examples/ to see what effects are possible), Wikimedia Commons (search the
  category pages, take the original file URL), NASA / NIH-NIAID (public domain), Fritzchens Fritz on Flickr (CC0 die
  shots), Poly Haven (CC0 HDRIs, models, textures), ambientCG (CC0 PBR), Smithsonian 3D (CC0), Natural Earth (public
  domain maps → globe textures, coastlines). Avoid: NC licences (e.g. TeleGeography's cable map is CC BY-NC-SA — draw
  schematic routes yourself and label them "schematic routes"), "editorial use only" press images in anything
  promotional, watermarked stock. Sketchfab downloads need a login — ask the user or model it procedurally.
- **3D recipes (Three.js, PBR + HDRI — ready-made in `templates/three-kit.js`)**: an object that comes apart into its real layers (exploded cross-section of a
  cable, a chip package: lid → die with the real die-shot photo as texture → substrate → balls); a globe with a Natural
  Earth land texture, glowing route arcs and a camera that flies between two cities; a long object lying on a textured
  floor (seabed sand, depth fog, light shafts) seen 3/4 so it reads at a glance; a message/light pulse travelling along
  it. Mark 3D heroes for the layout check with `window.FOCAL_BOXES`.
- **Photos in 9:16** (`scripts/prep_image.py card`): a card with the photo's OWN aspect ratio, full safe width, over a blurred darker copy of the same
  photo as background — never a thin strip with dark padding inside the card; crop out museum labels / watermarks.
- **Honest labels**: label what the image really is ("photo: <exact subject>", "3D illustration", "schematic routes").
- **Design pass before animation**: style frames for every beat, self-critiqued for density and fit (§5c), then animate.
- Three.js renders on the GPU (render.py launches Chromium with Metal + file:// access, ~20 ms/frame).
- **Render politely**: `nice -n 15`, `--workers 3`, render in slices and delete frames right after encoding — three
  parallel full renders pegged the user's Mac at 100 % CPU and filled the disk.

## 9. Review process
- People judge **animation, not stills or written plans**: never ask for approval on keyframes or a storyboard doc.
  Check stills yourself (contact sheets), then show a rendered video (a 30 fps half-res draft is fine for direction).
- For several versions, use **independent agents per version** (different story angles) to avoid idea bias.
- After rendering, **reveal the files in Finder** (`open -R` each file, or `open` the folder) and ask which one is best.
- **QC loop before showing anything** (Q16 "Extreme" = all of it, every render):
  `qc_video.py` (audio offset, Whisper transcript vs script, pauses, black/white/frozen frames, loudness, 4 fps sheets) +
  `qc_captions.py` (caption position stable at 60 fps, hold, on-time) + `render.py --sweep 10` (layout). Then READ every
  contact sheet yourself. Timing checks alone missed a caption that jumped sideways — check positions, not just times.
- Keep a running log (README.md in the output root): # / title / final path / status / why earlier versions were rejected.
