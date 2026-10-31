# Motion engines — skill timeline, HyperFrames, Remotion

All three work the same way underneath, the `seek(t)` model: every frame is a pure function of time, a headless
browser draws the frame at time t, FFmpeg encodes. So timing, copy, colours and layout can change without
regenerating anything. The agent picks one per video (SKILL.md Step 2b) — never ask the user which engine. Everything else in this skill (intake, brand extraction, narration,
SFX, craft.md, QC, reveal) applies to every engine.

| | Skill timeline | HyperFrames | Remotion |
|---|---|---|---|
| authoring | one HTML file, plain JS `seek(t)` | HTML + GSAP timelines, one scene per sub-composition | React components, `useCurrentFrame()` |
| strengths | Three.js kit, word-by-word `Captions()`, `EndCard()`, 240 fps capture + motion blur, layout sweep | ~450 registry blocks (transitions, kinetic type, charts, maps, captions, 3D), `capture <url>` of a site, `check` (layout, contrast, motion), `snapshot --review`, Studio + desktop app | props-driven templates, `<Player>`, Lambda/Cloud Run, big ecosystem (`@remotion/captions`, google-fonts, maps, three) |
| official skills | this skill | `/hyperframes` (read first), `/hyperframes-cli`, `/hyperframes-registry`, `/media-use` | `/remotion-best-practices` (router: create, markup, render, captions, maps, studio, saas) |
| licence | ours | Apache-2.0 | free for individuals / teams ≤ 3, company licence above (remotion.pro/license) |
| tested here | yes | 4 s 1080p in 11 s (v0.8.206) | 4 s 1080p in 16 s (v4.0.539) |

## Setup (once per machine; Node ≥ 22 + FFmpeg)
```bash
npx -y hyperframes@latest skills update                                   # /hyperframes, -cli, -registry, /media-use
npx -y skills add remotion-dev/skills -g -a claude-code -s remotion-best-practices -y
```
`scripts/check_env.sh` reports whether both are installed.

## HyperFrames
1. Load `/hyperframes` (its contract is strict — read it) and `/hyperframes-cli`.
2. Project per version: `npx hyperframes init <root>/options/<L>-<angle>` (blank). Product video: `npx hyperframes
   capture <url> --json` gives screenshots, assets, colours and fonts of the real site — use it alongside brand.md.
3. Formats: the root's `data-width`/`data-height` (1920×1080, 1080×1080, 1080×1350, 1080×1920). Compose each format
   natively (craft.md §5) — one project per format or variables switching the layout; never crop.
4. Before hand-building any effect, search the registry: `npx hyperframes catalog` / `add <block>` (`/hyperframes-registry`).
5. Brand fonts: anything outside its bundled list needs `@font-face` to a file in `assets/fonts/` (download the
   woff2 from Google Fonts / the site). Without it `check` fails with `font_family_without_font_face` and the render
   falls back to a generic font.
6. Audio: our `sfx.py` / `el_tts.py` / `mix.py` output WAVs → `<audio id="…" src="assets/…wav" class="clip" data-start
   data-duration>`; words.json from `el_tts.py` drives captions (or the registry's caption blocks, `/media-use` for
   transcripts).
7. Check + review: `npx hyperframes check --json --at-transitions` (fix every error) → `npx hyperframes snapshot
   --review` (read the frames, write REVIEW.md as `/hyperframes` asks) → our QC on the MP4 (`qc_video.py`, plus
   `review_frames.py`-style passes if QC = Extreme).
8. Render: drafts `npx hyperframes render --quality draft -o draft.mp4`; final `npx hyperframes render --fps 60
   --quality delivery -o <slug>_<platform>_<W>x<H>.mp4`. The user judges rendered animation (this skill's rule), so
   render drafts for review instead of stopping at the Studio preview; still mention they can keep editing in the
   HyperFrames desktop app.

## Remotion
1. Load `/remotion-best-practices` → `remotion-create` and `remotion-markup` references.
2. Project per version: `npx create-video@latest --yes --blank --no-tailwind <root>/options/<L>-<angle>`.
3. Formats: one `<Composition>` per format (same component, `width`/`height` per format, layout from
   `useVideoConfig()`); content as props (`defaultProps` / `--props`) so the same composition re-renders with new copy.
4. Motion: `spring()` and `interpolate()` on `useCurrentFrame()` — never `useState` timers or CSS transitions.
   Assets in `public/` via `staticFile()`; brand fonts via `@remotion/google-fonts` or local `@font-face`
   (`remotion-markup/local-fonts.md`) — unloaded fonts silently fall back.
5. Audio: `<Audio src={staticFile('narrated.wav')} />`; captions from words.json or `@remotion/captions`.
6. Review: `npx remotion still <Comp> --frame=<n> out.png` at the same timestamps as `render.py --test`, read them,
   then our QC on the MP4.
7. Render: `npx remotion render <Comp> out.mp4` (drafts: `--scale=0.5`; final at the composition's fps, set 60 for
   the delivery). The Remotion skill says "don't render unless asked" — in this skill the user judges rendered
   drafts, so render them.

## Choosing (the agent decides, says why in one line)
- Real 3D, exploded objects, globe routes, narrated stories with word-by-word captions → **skill timeline**.
- Product launch from a live site, kinetic type, charts, maps, many transitions, the user wants to keep editing
  visually → **HyperFrames**.
- A template that will be re-rendered with new data many times, or a React codebase that should own the video →
  **Remotion**.
