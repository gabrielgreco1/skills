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
- **Hook lines that held a 90 s explainer to the end** (the algorithm reel, PT-BR, approved 2026-10-28; the user had
  rejected "fica até o final"-style teases and a recorded sign-off as weak):
  · *Open loop that names a concrete extra item in the first narrated sentence*: "E eu vou colocar o TikTok no meio,
    porque ele ignora uma coisa que todo mundo acha que importa." The item gets its own act later; the loop stays open
    for 60 s.
  · *Aside in the on-camera hook*: the recorded hook names three things; the fourth appears handwritten over the
    footage ("+ o TikTok?") — curiosity without re-recording, and it tells the viewer the video goes beyond the title.
  · *Relatable setup* right after: "Pensa que você postou o mesmo vídeo nas quatro redes."
  · *Mid-video follow CTA* after ≥ 60 % of the value and immediately followed by a reason to stay: "E se você tá
    aprendendo alguma coisa, me segue no greco dev pra não perder os próximos. Porque agora vem o TikTok." On screen:
    the real profile card, a hand presses "Seguir" → "Seguindo ✓". The user: "o negócio de seguir tá num momento bom".
  · *The closing line turns the viewer's own behaviour into the proof of the last point*: "E no TikTok, prende até o
    último segundo. Que nem você fez agora." — with the reel's own progress bar completing on "agora" and a
    "visto até o fim" chip. No end card, no recorded sign-off after it.
  · *A connector opens every sentence* (Mas, Só que, Por isso, Então, Já no X…) and each act ends by opening the next
    ("Porque agora vem o TikTok").

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

## 3b. Make the motion look expensive (timing, not effects)
Most cheap-looking animation fails on timing and composition, not on a lack of effects. No generic AI gradients, no
excess glow, restrained colour, precise type. Template helpers (all pure functions of `t`):
- **Closed-form springs** — `spr(t)` is analytic, so any frame renders without simulating the ones before it. A value
  that changes target several times: `springKeys(t, [[t0,v0],[t1,v1],…])` = v0 + Σ Δv·spr(t − tᵢ). Never integrate a
  spring frame by frame (breaks `seek(t)` and slice renders). Keep springs restrained (z ≥ .55 for UI, little overshoot).
- **Animate edges, not rectangles** — a tab indicator/selection moves its leading edge first and its trailing edge a
  beat later (`edgeSpring(t, [[t,left,right],…])`): it stretches briefly and settles. Far more intentional than a
  rigid box sliding at constant speed.
- **Container first, text after** — when a button grows into a card, the box starts moving at tc; the old label is
  gone before tc and the new one arrives only once there's room (`swap(t, tc)` → {a, b} opacities). Overlapping labels
  inside a morphing box is the #1 tell of an unfinished AI UI animation.
- **Cursor on real UI** — the cursor travels on a spring (`springKeys` for x and y), presses (scale .96 → 1, ~0.12 s),
  and the UI reacts on the press frame (highlight, ring, state change), with a tick SFX on the same MARK.
- **Sound is part of the timeline** — attach clicks, chart completions, camera moves and logo reveals to MARKs, or to
  beats from `beat_map.py` when there is a track. Review the sound as carefully as the picture.

## 3c. Timing table of the approved product-UI reel (calm pacing, 60 fps)
| what | timing |
|---|---|
| card / panel / phone entrance | 0.55 s, 36–60 px rise, scale .94→1, slight overshoot (`E.oB(t,1.2)`) |
| exit | 0.30 s, −18 px, no overshoot; finished before the next entry in the same band |
| headline | fade + 18 px rise per word, 0.5 s, 0.05 s stagger; `tout` ≤ next `tin` − 0.55 s |
| section change | 0.45 s crossfade + 60 px slide; the stepper pill opens its label in 0.45 s |
| dim + blur behind a print | 0.35–0.40 s, together with the print; blur 14 px, 40 % tint |
| real print | enters at 860 px wide; the marker sweeps `scaleX 0→1` in 0.4 s on the spoken word |
| counters | 0.5–0.8 s per step, `E.o3`, tabular figures, a 1.08 pulse on each landing |
| bars / progress | 0.85 s `E.o3`; a bar that must land on a word uses `kv()` with `E.io3` to that word |
| toggles, segmented control, strike-through | 0.3–0.5 s `E.io3` |
| cursor / hand | `springKeys` f 1.6 z .7; press = 0.14 s scale .90, ring 0.7 s |
| caption words | pop 0.18 s; a chunk's last word stays ≥ 0.3 s; the next chunk may wait ≤ 0.18 s for it |

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
Split it into cues with the alignment afterwards. **Never edit the take**: no re-spacing the pauses, no splicing a line
from another take, no `atempo` speed-up — all three were done once and rejected ("a fala tá bugada", "a entonação de
uma frase não conecta com a próxima"). Only trim the head/tail. A wrong line or a script change (even one word) =
regenerate the WHOLE script in one request (~1,300 credits for 80 s).
Typical cost: ~1 credit per character (an 80 s script ≈ 1,300 credits) — test the hook line first (~150 credits).
**Always transcribe the result** (`qc_video.py`, Whisper) and diff it against the script before building the picture:
a take can misread a sentence so its meaning flips (a misplaced comma, a word read as a different word) — often
only the transcript catches it. Check pauses > 0.35 s inside sentences in the word timings.
**Check the head of the take by itself** (transcribe its first 1.5 s and look at the energy per 100 ms): a clone can
hallucinate a syllable before the first word — one take opened with ~0.8 s of "E aí, não sou eu" before "a resposta",
alignment labelled it as a 0.9 s "E", and the video shipped with it until the user heard "enum" at the start. The fix
that keeps the take intact: trim the head up to the first real word (15 ms fade), keep word 0 as a placeholder so
every word index stays valid, hide it from the captions, shorten DUR.

**Caption rules** (template `Captions()`, verified by `qc_captions.py` — every one of these was a visible bug):
- A chunk's layout is **static**: all its words are laid out when it appears (unspoken ones at opacity 0) — never
  add/remove words or re-centre while it's on screen (words jumped sideways and ghosted).
- Words a headline prints at the same moment are decided ONCE (a static hide set), never per frame.
- Chunks: one line, 2–4 words, never cross a sentence end, never split a spoken number ("noventa e oito palavras"),
  keep the script's punctuation; the last word stays readable ≥ ~0.3 s; a chunk leaves when the next spoken word
  starts — it never lingers over the next shot.
- Preload every font weight before `window.ready` — a weight first used mid-video loads late and re-flows the text.
- Caption plate = soft rounded backing behind the words only, never a full-width dark bar.
- Series style that replaced the plate (Gabriel's reels): white Inter 900, 7 px black stroke (`-webkit-text-stroke` +
  `paint-order: stroke fill`), soft shadow, no box, no colour change on the newest word. Chunks of up to 6 words /
  30 chars; the last word of a chunk never shows < 0.3 s (the next chunk waits ≤ 0.18 s) — `qc_captions.py` must
  report no SHORT HOLD; a few LATE ≤ 0.18 s are the accepted price.

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

## 8b. Illustrated-world explainer — the approved pattern (data-pipeline reel, 2026-10-27)
v1 (UI boxes on an empty beige frame) was rejected as "motion ridículo"; v2/v3 built like this were approved
("gostei bastante desse padrão de animação"), and v8 became the quality bar (max-quality.md). Use the principles for
any process / system / "how X works" explainer. The pipe, the stacked stations, the dashed map and the measurements
below are how THAT reel did it: invent the world, the path and the camera grammar for each new topic (max-quality.md §2).
- **One world, one path.** Stack full-bleed illustrated stations (1080×1920 each, flat vector with
  gradients and soft shadows), one per step, all joined by ONE physical path (a pipe, a road, a cable). The camera
  rides that path down between stations (eased 0.75 s moves) — no hard cuts inside the narration. Each station has its
  own background colour; a ground/soil strip between stations; decor (bushes, crates, furniture) fills the bleed zone
  below the captions so no frame has an empty bottom third.
- **Bands in every station (9×16):** stepper pill y≈300 · headline 2 lines at `SB.x`, y≈372, 84–92 px · hero visual
  600–1250 · captions 1270–1460 · decor below. Nothing readable left of `SB.x` (=150).
- **One object travels the whole video.** The same records/item change state at every station (raw → stored → cleaned →
  summarised → shown on the final screen); the numbers on the last screen match the ones built earlier.
- **Open on a concrete user action that creates the thing** — e.g. a food-delivery screen, a finger moving to
  "Fazer pedido", tap → "Pedido #82 ✓", and the order rides the path from top to bottom. "Pedir corrida" on a map was
  not clear enough: show the item, the price and the button.
- **A map of the same stations comes back** (vignettes = clones of the station SVGs + big numbered labels, inside a
  dashed frame with the umbrella step on a tab): when the parts are listed, when the process runs (night: vignettes
  dark, light up in order, the failing one turns red), and as the close (day, all ✓, the creator's photo on top).
  Leave ≥ 40 px between the tab and the first vignette; the tool's name gets its OWN chip, never stuffed into
  the tab. Vignette SVGs need their own def ids (`id="v<k>…"` + `url(#v<k>…)`): gradients referenced from a hidden scene
  don't render.
- **Every element pops on its spoken word.** Real prints enter big (≈940 px wide), one at a time, with the marker on the
  exact phrase, then leave or fly into the scene (the storage-price print shrinks into the lake's price sign).
- **Never stack cards over a busy scene.** When a print/alert must sit over the map, dim everything behind it (≈80 %
  dark overlay) and show only that card (+ one alert chip). "Soltou um monte de dado em cima do mesmo bagulho" = rejected.
- **Process diagrams = named step boxes**: big icon + verb ("Extrair", "Transformar", "Carregar"), arrows between, the item
  rides INSIDE the box it is in and that box lights up (border + slight scale); where a step happens is shown by a dashed
  frame labelled with the system ("data warehouse" around L in ETL, around L+T in ELT). Rejected: tiny icon clusters,
  data cards floating outside/above the boxes.
- **The final screen is a real-looking product UI**: top bar with name + time, KPI tiles that count up, a styled chart,
  a status list (e.g. the night's pipeline run with ✓ per step) — not a bare bar chart.
- **Detail check on props**: clip suns/views to their window, props stand ON a surface (mug, plant on the desk top), no
  element overlapping a frame/bezel by accident.
- **Engineering:** hide world HTML elements that are off-screen each frame (and restore them at the start of the next
  seek) — otherwise the layout sweep reports thousands of false "outside safe zone" errors.
- **Talking-head outro trims**: cut at a word onset found with RMS (20 ms windows) and confirm with Whisper on a 1.5 s
  test clip; re-link the JPEG frames from that frame on and shift the word timings.

## 8c. Talking-head hook: editorial caption collage + a "pull" into the video (approved direction, 2026-10-27)
Reference the user liked (a dev creator's Reels): the hook's captions are NOT a running subtitle band.
- Curated: show some words, sometimes wait for the phrase to finish; every word shown pops on its spoken time and a
  block stays while the phrase lasts. Place the block in a free area (above the head when the face is mid-frame).
- Mixed type inside one block: bold sans for the setup ("você sabe como funciona"), italic serif for the middle
  (Instrument Serif), ONE giant condensed keyword in yellow (Anton, "PIPELINE"), handwriting with a drawn arrow
  (Caveat), and editor gimmicks: a selection box with handles that a cursor drags over the words being said, a typing
  caret. Soft shadow, no boxes.
- End the hook with a pull into the motion: an object related to the topic appears (a folder named after the video),
  a cursor double-clicks it, and it opens as a window that grows to full frame with the motion inside — the narration
  starts inside that window. Other pulls that fit: an arm pulling something into frame, a file being dragged.
- The motion must not repeat the voice literally: when the narration says "um gráfico, um relatório ou um modelo",
  show what that business really sees (an orders chart drawing itself, the month's report landing, a forecast line)
  — never tiles labelled with the spoken words.

- **Measure the head first.** Draw a 100 px grid over a real hook frame (`PIL`) and keep every collage row above the
  hairline; move rows, not the footage. The pull object (a phone, a folder) rises over the chest at ~60 % size and
  travels to its place in scene 1 while the footage fades — a match cut, not a wipe. An aside that the voice never
  says ("+ o TikTok?") goes under the "vem comigo" block, in the free band between the collage and the head.

## 8d. Product-UI world — the approved pattern for software / platform / algorithm topics (2026-10-28)
Two illustrated worlds (a bench of instruments, a factory with a conveyor) were rejected from stills for the same
topic; the product-UI world was approved from the render. Full method and checklist: max-quality.md §2b. In short:
real phones with the real app screens, one hero panel per act in that platform's own design language, real prints
with the marker on the spoken phrase, the math on screen, a studio background per brand, one travelling subject and one
recurring device. Components in `templates/ui-kit.js` (phone, studio, stepper, print card, report card, outlined
captions, `pop/vo/kv/hlB`).

## 9. Review process
- People judge **animation, not stills or written plans**: never ask for approval on keyframes or a storyboard doc.
  Check stills yourself (contact sheets), then show a rendered video (a 30 fps half-res draft is fine for direction).
- For several versions, use **independent agents per version** (different story angles) to avoid idea bias.
- After rendering, **reveal the files** (`bash $SKILL/scripts/reveal.sh <file>`; Finder / Explorer / xdg-open) and ask
  which one is best.
- **Exception, quality "Maximum" only**: the style-frame sheet goes to the user once, with one question about the
  direction, before animating (max-quality.md §4). A direction change after animating costs hours.
- **QC loop before showing anything** (QC "Extreme", from quality Maximum or High = all of it, every render):
  `qc_video.py` (audio offset, Whisper transcript vs script, pauses, black/white/frozen frames, loudness, 4 fps sheets) +
  `qc_captions.py` (caption position stable at 60 fps, hold, on-time) + `render.py --sweep 10` (layout). Then READ every
  contact sheet yourself. Timing checks alone missed a caption that jumped sideways — check positions, not just times.
- **QC "Extreme": five passes, in order** (`scripts/review_frames.py` builds the sheets + `review_report.md`):
  1 *storyboard* — 12 frames over the whole timeline: one coherent story? · 2 *timing* — every MARK at −0.12 / +0.06 /
  +0.30 s: overlapping text, jumps, things vanishing mid-move (a contact sheet at regular intervals misses what breaks
  BETWEEN its frames) · 3 *phone size* — the frames at ~390 px wide, as people watch: still readable? · 4 *brand + facts*
  — logo, font, colours, real screenshots, every number from an approved claim · 5 *encoded file + audio* — 1 fps
  contact sheet of the MP4, ffprobe size/fps/duration, SFX sync, loudness.
- **A review report, not a verdict.** Never say "the animation looks great" without having opened the rendered frames.
  The report lists the timestamps inspected, issues found, fixes applied, remaining concerns — and a human approval
  box that must be ticked before anything is delivered. Model visual review is good, not perfect.
- The polished result is rarely the first one (a widely shared one-prompt-looking film took 163 model calls and hours).
  Budget iterations; don't oversell a first render.
- Keep a running log (README.md in the output root): # / title / final path / status / why earlier versions were rejected.
- **Order that worked for the algorithm reel** (and three restarts of the final render were still needed): scene sheet
  → user gate → animate → `render.py --sweep 10` until `layout: OK` (copy render.py without its 60-line cap and group
  the messages by text to see every problem) → `qc_captions.py` until no SHORT HOLD → 30 fps half-res draft → stills at
  every MARK (−0.12 / +0.3 / +0.9 s) read as contact sheets → `render_final.sh` → `qc_video.py` (its AUDIO OFFSET
  assumes the take starts at 0 s; with an on-camera hook cross-correlate from `OFF` yourself) → read all 4 fps sheets →
  `review_frames.py --mp4` → fill the report. Anything found in a sheet is fixed before the user sees the file.
