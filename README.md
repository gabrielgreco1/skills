# skills

A growing pile of [Claude Code](https://claude.com/claude-code) skills: drop-in folders that teach your agent to do one thing really, really well.

Right now the pile has exactly one skill in it. It's a very good skill, though, and more are coming.

> ⭐ **If this saves you an afternoon, leave a star.** It costs nothing and helps other people find the repo.

## The skills

| Skill | What it does |
|---|---|
| [`motion-designer`](./motion-designer) | Turns a product website, or any story or topic, into short motion-graphics videos for Reels, TikTok, Shorts, Instagram, LinkedIn and X. You get real photos, real 3D, captions that appear word by word as they're spoken, natural narration, sound design and a spoken call to action. Everything is rendered from code: no After Effects, no timeline scrubbing. Each video is checked frame by frame before you see it. Before it starts, it asks you a few questions: language, idea, how many versions, sound, voice, platform and length. |

*Some skills are on their way. Some are still just a strongly worded note on my phone.*

## Install a skill

```bash
git clone https://github.com/gabrielgreco1/skills.git
cp -r skills/motion-designer ~/.claude/skills/
```

Then open Claude Code and just ask, e.g. *"make a motion video about how coffee gets from the farm to your cup"*, or call it with `/motion-designer`. Each skill's own README lists what you need to install for it.

## FAQ

**Does it really make the video, or just a plan for one?**
It makes the actual MP4s, more than one version if you want, and opens them in Finder so you can pick a favourite.

**Will it burn my CPU?**
For a little while, yes. 240 fps renders are no joke. It runs at low priority and cleans up after itself, so your laptop will survive. Your fans will have opinions.

**Can I contribute a skill?**
Yes. Open a PR with a folder that contains a `SKILL.md`. Bonus points if every rule in it came from a mistake you made yourself.

## License

Use the skills, change them, ship videos with them. The vendored third-party code keeps its own license (Three.js is MIT).
