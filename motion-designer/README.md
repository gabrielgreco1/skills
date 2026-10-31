# motion-designer — a Claude Code skill for real motion-graphics videos

Turns a product site, a story/topic or a song into short, shareable MP4s (Reels/TikTok/Shorts, Instagram, LinkedIn, X):
real photos + Three.js 3D + word-by-word captions + natural narration + sound design + a spoken CTA — rendered
frame-perfect from code (no After Effects), then checked frame by frame before you see it.

## Install
1. Copy this folder into your agent's skills directory — `~/.claude/skills/motion-designer/` (Claude Code),
   `~/.agents/skills/motion-designer/` (Agents-compatible clients), `~/.omp/skills/` (omp), or your project's
   equivalent.
2. Tools — macOS, Linux and Windows (git-bash/WSL). `scripts/check_env.sh` prints the exact command for your system:
   ```bash
   # system packages
   brew install ffmpeg potrace            # macOS
   sudo pacman -S ffmpeg potrace          # Arch (apt-get / dnf equivalents work the same)
   # python
   pip3 install numpy pillow playwright edge-tts && python3 -m playwright install chromium
   # recommended extras: transcript QC + photo cut-outs
   pip3 install mlx-whisper               # Apple Silicon (fast)
   pip3 install openai-whisper            # any platform, CPU or CUDA — qc_video.py picks whichever is installed
   pip3 install rembg
   ```
   Then run `bash scripts/check_env.sh`.
3. Optional — ElevenLabs (much more natural narration): a key with *Text to Speech* + *Voices: Read*, on a paid plan
   (free plans can't use library voices via the API and have no commercial licence). The skill asks for it and stores
   it in `~/.config/elevenlabs/api_key`.
4. In your agent: "make a motion video about …" or `/motion-designer`. The first question is the language
   (Português / English / Español / other); everything after follows it.
5. Rendering on a headless box: `NO_OPEN=1` stops the skill from revealing files in the file manager
   (`scripts/reveal.sh` is what does it — Finder, Explorer or `xdg-open`).

## What's inside
| path | what |
|---|---|
| `SKILL.md` | the workflow and the full intake (language → type → look → idea → versions/sound/narration/platform → duration/visuals/CTA/engine → voice/captions → quality level (Maximum / High / Quick draft) → hook/retention/pacing) |
| `references/craft.md` | the quality bar — every rule came from a rejected draft |
| `references/max-quality.md` | the "Maximum" level: the method behind the best video so far (invent the world, style-frame gate, designed props, self-review loop) |
| `references/pipeline.md` | step-by-step production commands |
| `references/brainstorm.md` | formats for products and for story/curiosity content |
| `templates/beat-edit.html` + `references/beat-edit.md` | beat edits: music-driven hype edits (cuts on every bass hit, drop, giant word slams, strobe, grain) — `beat_map.py`, `slowed_reverb.py`, `vectorize_logo.sh` |
| `templates/timeline.html` | deterministic timeline: safe zones, layout bands, `Captions()`, `EndCard()` |
| `templates/ui-kit.js` | product-UI world components (phones, studio backgrounds, stepper, print cards with marker, report card, outlined captions, timing helpers) — the pattern approved for software/platform topics |
| `templates/three-kit.js` + `lib/three/` | Three.js r170 (MIT, vendored) + ready 3D recipes: exploded layers, globe with routes, seabed + cable with a light pulse, bloom, HDRI lighting |
| `scripts/fetch_assets.py` | three.js examples library, Wikimedia Commons, Poly Haven, NASA — licence logged per file |
| `scripts/prep_image.py` | photo cards for 9:16, cut-outs, grading, grain |
| `scripts/el_voices.py` · `el_tts.py` · `vo.py` | voice previews (free) · one-take ElevenLabs narration with word timings · edge-tts |
| `scripts/render.py` · `render_final.sh` · `render_all.sh` · `encode.sh` | frame capture + layout checks · low-impact final render · all formats |
| `scripts/qc_video.py` · `qc_captions.py` | final QC: audio offset, transcript vs script, pauses, frames, loudness, caption stability |
| `references/campaign.md` · `scripts/validate_campaign.py` · `render_campaign.py` | campaign mode (optional, asked in the intake): brief as data, validated (assets, fonts, lengths, sourced claims), hooks × formats × CTAs from one timeline with cached segments, posters, manifest |
| `references/engines.md` | other engines the agent picks per video: HyperFrames (HTML + GSAP, registry blocks) and Remotion (React) — setup, intake mapping, gotchas; uses their official skills |
| `scripts/review_frames.py` | 5-pass review (QC "Extreme", quality Maximum/High): storyboard, transitions, phone-size, encoded contact sheet + review report |

Renders are CPU/GPU heavy (240 fps capture → 60 fps with motion blur): the scripts run niced, 3 workers, in slices,
and delete frames as they go (~2 GB peak). Asset licences: credit every CC BY / BY-SA file in the post caption.
