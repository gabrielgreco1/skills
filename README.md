# skills

A growing pile of [Claude Code](https://claude.com/claude-code) and [Codex](https://developers.openai.com/codex/) skills: drop-in folders that teach your agent to do one thing really, really well.

Right now the pile has five skills in it, and more are coming.

> ⭐ **If this saves you an afternoon, leave a star.** It costs nothing and helps other people find the repo.

## The skills

| Skill | What it does |
|---|---|
| [`motion-designer`](./motion-designer) | Turns a product website, or any story or topic, into short motion-graphics videos for Reels, TikTok, Shorts, Instagram, LinkedIn and X. You get real photos, real 3D, captions that appear word by word as they're spoken, natural narration, sound design and a spoken call to action. Everything is rendered from code: no After Effects, no timeline scrubbing. Each video is checked frame by frame before you see it. Before it starts, it asks you a few questions: language, idea, how many versions, sound, voice, platform and length. |
| [`webscraping-expert`](./webscraping-expert) | The whole playbook for getting data off a website or API. Starts with a short intake, then always tries the cheapest path first — a plain HTTP request before a browser — and only climbs the ladder when it has to: TLS/HTTP fingerprint impersonation, the modern stealth-browser stack, the anti-bot vendor matrix (Cloudflare, DataDome, Akamai, Kasada) with a bypass per vendor, CAPTCHA solving, proxy networks and managed unblockers with geo-targeting, and structured data (JSON-LD) the site hands you for free. Includes site-stack playbooks (Next.js/RSC, Natural for Ajax, Tableau, OData, GraphQL, ASP.NET, SPAs and more), HAR-driven discovery with exact stateful-request replay and fidelity checks, document extraction (PDF/XLSX/OCR), resumable runs, and a neutral recon report at the end. |
| [`agentbox`](./agentbox) | Runs web-scraping subagents inside isolated Docker sandboxes, one box per subagent. Each box has a terminal, a persistent headless Chromium, passive listeners that log every request without touching the traffic, and an optional proxy from any provider with a hard budget and known cost per request. An agent journal and a merged timeline let you check every claim a subagent makes before you trust it. Needs Docker. |
| [`aula-interativa`](./aula-interativa) | Turns any topic into a self-contained HTML lesson with interactive slides, worked examples and deterministic animations checked frame by frame with Playwright. Asks only for language, topic and depth (or a slide count). Includes detailed teaching and motion guides, ten animation recipes, a reusable player, frame capture, contact sheets and artifact-bound review reports. Software lessons connect concepts to version-labelled UI walkthroughs. |
| [`ui-humanizer`](./ui-humanizer) | Takes the "made with AI" look out of sites, landing pages, apps, docs and slides. Built from 51 replies to a thread on what gives an AI-made site away: the uppercase label above every heading, the gradient word in the title, cards with a side stripe, pulsing chips, emoji as icons, Tailwind purple, pills everywhere, a bakery that looks like a SaaS. It runs a full process (brief, sketch before code, references from Pinterest and friends searched in the browser, design system, build, audit) and ships a dependency-free detector script. |

*Some skills are on their way. Some are still just a strongly worded note on my phone.*

## Install a skill

```bash
git clone https://github.com/gabrielgreco1/skills.git
cp -r skills/motion-designer ~/.claude/skills/
```

Or with the [skills CLI](https://skills.sh): `npx skills add gabrielgreco1/skills --skill agentbox`.

Then open Claude Code and just ask, e.g. *"make a motion video about how coffee gets from the farm to your cup"*, or call it with `/motion-designer`. Each skill's own README lists what you need to install for it.

For interactive lessons, install `aula-interativa` instead. Its [README](./aula-interativa/README.md) includes Claude Code and Codex setup.

## FAQ

**Does motion-designer really make the video, or just a plan for one?**
It makes the actual MP4s, more than one version if you want, and opens them in Finder so you can pick a favourite.

**Will motion-designer burn my CPU?**
For a little while, yes. 240 fps renders are no joke. It runs at low priority and cleans up after itself, so your laptop will survive. Your fans will have opinions.

**Can I contribute a skill?**
Yes. Open a PR with a folder that contains a `SKILL.md`. Bonus points if every rule in it came from a mistake you made yourself.

## License

Use the skills, change them, ship videos with them. The vendored third-party code keeps its own license (Three.js is MIT).
