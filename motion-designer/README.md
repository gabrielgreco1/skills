# motion-designer — a Claude Code skill for real motion-graphics videos

Turns a product site, a story/topic or a song into short, shareable MP4s (Reels/TikTok/Shorts, Instagram, LinkedIn, X):
real photos + Three.js 3D + word-by-word captions + natural narration + sound design + a spoken CTA — rendered
frame-perfect from code (no After Effects), then checked frame by frame before you see it.

## Install
1. Copy this folder to `~/.claude/skills/motion-designer/` (or your project's `.claude/skills/`).
2. Tools (macOS, Apple Silicon recommended):
   ```bash
   brew install ffmpeg
   pip3 install numpy pillow playwright edge-tts && python3 -m playwright install chromium
   pip3 install mlx-whisper rembg        # recommended: transcript QC + photo cut-outs
   ```
   Then run `bash scripts/check_env.sh`.
3. Optional — ElevenLabs (much more natural narration): a key with *Text to Speech* + *Voices: Read*, on a paid plan
   (free plans can't use library voices via the API and have no commercial licence). The skill asks for it and stores
   it in `~/.config/elevenlabs/api_key`.
4. In Claude Code: "make a motion video about …" or `/motion-designer`. The first question is the language
   (Português / English / Español / other); everything after follows it.

## What's inside
| path | what |
|---|---|
| `SKILL.md` | the workflow and the full intake (language → type → look → idea → versions/sound/narration/platform → duration/visuals/CTA/engine → voice/captions → hook/retention/pacing/QC) |
| `references/craft.md` | the quality bar — every rule came from a rejected draft |
| `references/pipeline.md` | step-by-step production commands |
| `references/brainstorm.md` | formats for products and for story/curiosity content |
| `templates/beat-edit.html` + `references/beat-edit.md` | beat edits: music-driven hype edits (cuts on every bass hit, giant words, recreated chat opener, offer lockup) — `beat_map.py`, `slowed_reverb.py`, `vectorize_logo.sh` |
| `templates/timeline.html` | deterministic timeline: safe zones, layout bands, `Captions()`, `EndCard()` |
| `templates/three-kit.js` + `lib/three/` | Three.js r170 (MIT, vendored) + ready 3D recipes: exploded layers, globe with routes, seabed + cable with a light pulse, bloom, HDRI lighting |
| `scripts/fetch_assets.py` | three.js examples library, Wikimedia Commons, Poly Haven, NASA — licence logged per file |
| `scripts/prep_image.py` | photo cards for 9:16, cut-outs, grading, grain |
| `scripts/el_voices.py` · `el_tts.py` · `vo.py` | voice previews (free) · one-take ElevenLabs narration with word timings · edge-tts |
| `scripts/render.py` · `render_final.sh` · `render_all.sh` · `encode.sh` | frame capture + layout checks · low-impact final render · all formats |
| `scripts/qc_video.py` · `qc_captions.py` | final QC: audio offset, transcript vs script, pauses, frames, loudness, caption stability |

Renders are CPU/GPU heavy (240 fps capture → 60 fps with motion blur): the scripts run niced, 3 workers, in slices,
and delete frames as they go (~2 GB peak). Asset licences: credit every CC BY / BY-SA file in the post caption.
