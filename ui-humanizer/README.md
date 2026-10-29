# ui-humanizer — take the "made with AI" look out of a UI

Some sites you open and know in two seconds an AI made them: the tiny uppercase label above every heading, one word of the title in a gradient, cards with a coloured stripe on the left, a chip with a pulsing green dot, emoji as icons, Tailwind's default purple, pills everywhere, a bakery that looks like a SaaS.

This skill was built from the [51 replies](https://x.com/greco_dev/status/2112133909458960896) to a thread asking people what gives an AI-made site away. Every reply is mapped to the place in the skill where it ended up (`references/cobertura.md`).

It is a process, not just a list of bans. Most of the replies agreed that swapping one cliché for another (purple → beige with Playfair italics) only makes it more obvious, and that a skill can't help without a brief, real material and references. So the skill walks the agent through: brief → sketch before code → references (Pinterest, Dribbble, Siteinspire… searched in the browser) → a minimal design system → build → audit with a detector → iterate, with the user choosing the direction.

Each page is also calibrated before a pixel is drawn: what the visitor is there to do (persuade, operate, read, showcase) sets a starting point on three observable axes — how far the composition departs from the template, how much moves, how dense it is — and that reading is checked against the rendered result at the end. Alongside the bans there is now the other half: the concrete numbers for type, spacing, colour and hierarchy, and a toolbox of composition and motion patterns worth reaching for, each with the point where it tips back into a tell. Durable decisions live in a per-project `DESIGN.md` so the next session doesn't start from the default again.

The skill is written in Portuguese. It works on any language UI.

## Install

```bash
npx skills add gabrielgreco1/skills --skill ui-humanizer
```

Or copy this folder to `~/.claude/skills/ui-humanizer/` or `~/.codex/skills/ui-humanizer/`.

Then ask *"deixa esse site menos com cara de IA"*, *"audit this landing page for AI tells"*, or call `/ui-humanizer`.

## What is included

| Path | Purpose |
|---|---|
| `SKILL.md` | Principles, the 8-phase process, final checklist and what to return |
| `metodo/calibragem.md` | Page intent (persuade/operate/read/showcase) and the three intensity axes with observable levels; the one-line reading that closes the brief |
| `references/tells.md` | The catalogue: 13 strong tells (act on one sighting), 11 that count in groups, 9 weak alone, plus 14 extensions seen outside the thread. Each with how to spot it, its code signature, why AI does it, who mentioned it, the fix and when it's fine to keep |
| `references/referencias.md` | How to find, filter and use visual references: sources (tested logged-out), search terms, how to discard AI-generated references, a reference sheet, directions, and the image-to-code route |
| `craft/fundamentos.md` | The concrete numbers behind "do this instead": type scale, spacing scale, colour structure, hierarchy, measure, motion, dark mode |
| `craft/padroes.md` | Composition and motion patterns worth reaching for, each with the point where it tips into a tell |
| `references/copy.md` | Interface copy that gives AI away, in Portuguese and English |
| `projeto/briefing-de-design.md` | The per-project `DESIGN.md` as a durable source of truth, with a machine-readable token block and a decision log |
| `qa/revisao.md` | Rendered review at three viewports, accessibility checks, severity-tagged report |
| `references/casos.md` | Three real sites from the thread taken apart tell by tell, with what to change first |
| `references/outros-formatos.md` | The same signature in docs, slides, dashboards and e-mails |
| `references/cobertura.md` | Every reply in the thread → where it lives in the skill |
| `references/comentarios.md` | The replies, verbatim |
| `scripts/audit.py` | Grep-based detector for the tells that have a code signature (HTML, CSS, Tailwind, JSX, Vue, Svelte, Astro) |

## The detector

```bash
python3 -I ui-humanizer/scripts/audit.py path/to/site
```

Prints `file:line [ID] tell | snippet` and a summary. No dependencies. It only finds what shows up in code; layout, missing images and the SaaS-for-everything structure need a look at the rendered page, which the skill does with a browser when one is available.
